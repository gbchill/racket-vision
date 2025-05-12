import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import uuid
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_video(video_path):
    """
    Process a video with MediaPipe pose detection
    Returns the path to the processed video
    """
    try:
        logger.info(f"Processing video: {video_path}")
        
        # Create a unique ID for the processed video
        unique_id = str(uuid.uuid4())
        
        # Create a temporary output file
        output_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        output_path = output_file.name
        output_file.close()
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Error opening video file: {video_path}")
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(f"Video properties: {width}x{height} at {fps} fps, {frame_count} frames")
        
        # Create VideoWriter object - use a different codec for Mac
        # For Mac use 'avc1' instead of 'mp4v'
        if os.uname().sysname == 'Darwin':  # Check if running on MacOS
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
        else:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Initialize MediaPipe Pose with specific configuration
        # We need to ensure we're providing the correct image dimensions
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,  # 0=Lite, 1=Full, 2=Heavy
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            
            frame_idx = 0
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break
                
                # Convert the image to RGB and process it with MediaPipe
                # The image dimensions are explicitly passed
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Set image for processing
                results = pose.process(image_rgb)
                
                # Draw pose landmarks on the image
                if results.pose_landmarks:
                    # Draw the pose landmarks on the image
                    mp_drawing.draw_landmarks(
                        image, 
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                
                # Write the frame to the output video
                out.write(image)
                
                # Print progress every 30 frames
                frame_idx += 1
                if frame_idx % 30 == 0:
                    logger.info(f"Processed {frame_idx}/{frame_count} frames ({frame_idx/frame_count*100:.1f}%)")
        
        # Release video resources
        cap.release()
        out.release()
        logger.info(f"Video processing completed. Output saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise