# Import necessary libraries
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import uuid
import platform  # For cross-platform OS detection
from pathlib import Path
import logging

# Set up logging to track the progress and any issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_tennis_video(input_video_path):
    """
    Process a tennis video with MediaPipe pose detection.
    This function takes a video file, analyzes it frame by frame to detect body poses,
    and creates a new video with pose landmarks overlaid.
    
    Args:
        input_video_path: Path to the input video file
        
    Returns:
        Path to the processed output video file
    """
    try:
        # Log that we're starting to process the video
        logger.info(f"Starting to process video: {input_video_path}")
        
        # Create output directory if it doesn't exist
        input_path = Path(input_video_path)
        output_dir = input_path.parent.parent / "tennis-videos-processed"
        output_dir.mkdir(exist_ok=True)
        
        # Create output filename with the original name plus a suffix
        output_filename = f"{input_path.stem}-processed{input_path.suffix}"
        output_path = output_dir / output_filename
        
        # Convert to string for OpenCV
        output_path_str = str(output_path)
        
        # Log the output path
        logger.info(f"Output will be saved to: {output_path_str}")
        
        # Open the input video file
        cap = cv2.VideoCapture(str(input_video_path))
        
        # Check if the video file was opened successfully
        if not cap.isOpened():
            logger.error(f"Error opening video file: {input_video_path}")
            raise ValueError(f"Could not open video file: {input_video_path}")
        
        # Get video properties
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
            if not cv2.VideoWriter(output_path_str, fourcc, fps, (width, height)).isOpened():
                logger.info("H264 codec not available, trying avc1")
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                
                # If avc1 also fails, fall back to mp4v with an FFMPEG conversion later
                if not cv2.VideoWriter(output_path_str, fourcc, fps, (width, height)).isOpened():
                    logger.info("avc1 codec not available, falling back to mp4v")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Create a VideoWriter with the new output path
        out = cv2.VideoWriter(output_path_str, fourcc, fps, (width, height))
        
        # Initialize MediaPipe Pose
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        
        # Set up the pose detector with specific settings
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
                
                # Convert to RGB and process with MediaPipe
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)
                
                # Draw pose landmarks on the image
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image, 
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    
                    # You could analyze the tennis form here
                    # image, feedback = analyze_tennis_form(results, image)
                
                # Write the frame to the output video
                out.write(image)
                
                # Print progress every 30 frames
                frame_idx += 1
                if frame_idx % 30 == 0:
                    logger.info(f"Processed {frame_idx}/{frame_count} frames ({frame_idx/frame_count*100:.1f}%)")
        
        # Release video resources
        cap.release()
        out.release()
        logger.info(f"Video processing completed. Output saved to: {output_path_str}")
        
        return output_path_str
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise

def analyze_tennis_form(results, frame):
    """
    Analyze tennis form based on the pose landmarks.
    This is where you would add tennis-specific analysis.
    
    Args:
        results: The pose landmarks from MediaPipe
        frame: The current video frame
        
    Returns:
        frame: The frame with analysis visualization
        feedback: Text feedback about the tennis form
    """
    feedback = []
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # Example: Check if the elbow is extended properly
        right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
        
        # Here you would calculate the angle and compare to ideal range
        
        # Placeholder for feedback
        feedback.append("Keep your eye on the ball")
        feedback.append("Follow through with your swing")
        
        # Add feedback text to the frame
        y_position = 30
        for text in feedback:
            cv2.putText(frame, text, (10, y_position), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_position += 30
    
    return frame, feedback

# If this script is run directly (not imported)
if __name__ == "__main__":
    # Use parent directory to access the tennis-videos folder
    input_video = Path("..") / "tennis-videos" / "tennis-forehand-1.mp4"
    
    # Check if the file exists before trying to process it
    if not input_video.exists():
        print(f"Error: File does not exist at path: {input_video.absolute()}")
    else:
        try:
            output_video = process_tennis_video(input_video)
            print(f"Processing complete! Output saved to: {output_video}")
            
            # Optionally, open the video with the default player
            import subprocess
            try:
                # This will open the video with the default video player on Windows
                subprocess.Popen(['start', output_video], shell=True)
                print("Opening the processed video...")
            except Exception as e:
                print(f"Could not open the video automatically: {str(e)}")
                
        except Exception as e:
            print(f"Error: {str(e)}")