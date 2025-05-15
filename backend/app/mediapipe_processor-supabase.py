import cv2
import mediapipe as mp

import numpy as np
import tempfile
import os
import uuid
import platform
from pathlib import Path
import logging

#set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#initialize mediapipe pose
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
        
        #create a unique id for the processed video
        unique_id = str(uuid.uuid4())
        
        #create a temporary output file
        output_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        output_path = output_file.name
        output_file.close()
        
        #open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Error opening video file: {video_path}")
            raise ValueError(f"Could not open video file: {video_path}")
        
        #get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(f"Video properties: {width}x{height} at {fps} fps, {frame_count} frames")
        
        # Use H264 codec for Windows which is more web-compatible
        if platform.system() == 'Darwin':  # check if running on macOS
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
        else:
            # For Windows, use H264 instead of mp4v
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            # If H264 is not available, try these alternatives
            # First try with avc1 which might work on some Windows installations
            if not cv2.VideoWriter(output_path, fourcc, fps, (width, height)).isOpened():
                logger.info("H264 codec not available, trying avc1")
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                
                # If avc1 also fails, fall back to mp4v with an FFMPEG conversion later
                if not cv2.VideoWriter(output_path, fourcc, fps, (width, height)).isOpened():
                    logger.info("avc1 codec not available, falling back to mp4v")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        #initialize mediapipe pose with specific configuration
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
                
                #image to rgb and process it with mediaPipe
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                #image for processing
                results = pose.process(image_rgb)
                
                #draw pose landmarks on the image
                if results.pose_landmarks:
                    #draw the pose landmarks on the image
                    mp_drawing.draw_landmarks(
                        image, 
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                
                #write the frame to the output video
                out.write(image)
                
                #print progress every 30 frames
                frame_idx += 1
                if frame_idx % 30 == 0:
                    logger.info(f"Processed {frame_idx}/{frame_count} frames ({frame_idx/frame_count*100:.1f}%)")
        
        #release video resources
        cap.release()
        out.release()
        logger.info(f"Video processing completed. Output saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise
