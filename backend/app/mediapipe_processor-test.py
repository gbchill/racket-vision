import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import uuid
import platform
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MediaPipe pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_video(video_path):
    """
    Process a video with MediaPipe pose detection
    Optimized for Supabase upload limits and web compatibility
    Returns the path to the processed video
    """
    try:
        logger.info(f"Processing video: {video_path}")
        
        # Create a temporary output file
        output_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        output_path = output_file.name
        output_file.close()
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(f"Original: {original_width}x{original_height} at {original_fps} fps, {frame_count} frames")
        
        # Compression settings for Supabase (balanced for quality and size)
        max_dimension = 640  # Slightly higher for better quality
        target_fps = min(24, original_fps)  # Keep reasonable FPS
        
        # Calculate new dimensions maintaining aspect ratio
        aspect_ratio = original_width / original_height
        if original_width > original_height:
            new_width = min(max_dimension, original_width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(max_dimension, original_height)
            new_width = int(new_height * aspect_ratio)
        
        # Ensure even dimensions (required for many codecs)
        new_width = new_width - (new_width % 2)
        new_height = new_height - (new_height % 2)
        
        logger.info(f"Output: {new_width}x{new_height} at {target_fps} fps")
        
        # Try different codecs for best compatibility
        codec_options = [
            ('avc1', cv2.VideoWriter_fourcc(*'avc1')),  # H.264 - best for web
            ('H264', cv2.VideoWriter_fourcc(*'H264')),  # Alternative H.264
            ('mp4v', cv2.VideoWriter_fourcc(*'mp4v')),  # Fallback
        ]
        
        fourcc = None
        out = None
        
        # Try codecs until we find one that works
        for codec_name, codec_fourcc in codec_options:
            fourcc = codec_fourcc
            out = cv2.VideoWriter(output_path, fourcc, target_fps, (new_width, new_height))
            if out.isOpened():
                logger.info(f"Using codec: {codec_name}")
                break
            out.release()
        
        if not out or not out.isOpened():
            raise ValueError("Could not create output video file with any codec")
        
        # Initialize MediaPipe pose with optimized settings
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,  # Lite model for speed
            smooth_landmarks=True,
            enable_segmentation=False,  # Disable segmentation for speed
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            
            frame_idx = 0
            frames_written = 0
            frame_skip = int(original_fps / target_fps) if original_fps > target_fps else 1
            
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break
                
                # Skip frames to achieve target FPS
                if frame_idx % frame_skip != 0:
                    frame_idx += 1
                    continue
                
                # Resize frame
                frame_resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
                
                # Convert BGR to RGB for MediaPipe processing
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                
                # To improve performance, mark the image as not writeable
                frame_rgb.flags.writeable = False
                results = pose.process(frame_rgb)
                
                # Convert back to BGR for OpenCV and make writeable
                frame_rgb.flags.writeable = True
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                
                # Draw pose landmarks
                if results.pose_landmarks:
                    # Draw landmarks with custom styling
                    mp_drawing.draw_landmarks(
                        frame_bgr,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(
                            color=(0, 255, 0),  # Green landmarks
                            thickness=1,         # Reduced from 2 to 1
                            circle_radius=1      # Changed from 2 to 1 (much smaller)
                        ),
                        connection_drawing_spec=mp_drawing.DrawingSpec(
                            color=(0, 255, 255),  # Yellow connections
                            thickness=2,
                            circle_radius=1      # Reduced from 2 to 1
                        )
                    )
                    
                    # Add frame info overlay
                    cv2.putText(
                        frame_bgr,
                        f"Frame: {frames_written}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
                    )
                
                # Write the processed frame
                out.write(frame_bgr)
                frames_written += 1
                frame_idx += 1
                
                # Progress logging
                if frames_written % 30 == 0:
                    progress = (frame_idx / frame_count) * 100
                    logger.info(f"Processing: {progress:.1f}% ({frames_written} frames written)")
        
        # Release resources
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        # Verify output file
        if not os.path.exists(output_path):
            raise ValueError("Output file was not created")
        
        output_size = os.path.getsize(output_path)
        if output_size == 0:
            raise ValueError("Output file is empty")
        
        output_size_mb = output_size / (1024 * 1024)
        
        # Verify the output video can be opened
        test_cap = cv2.VideoCapture(output_path)
        if not test_cap.isOpened():
            raise ValueError("Output video cannot be opened")
        
        test_frame_count = int(test_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        test_cap.release()
        
        logger.info(f"Processing complete: {output_size_mb:.2f} MB, {frames_written} frames written, {test_frame_count} frames verified")
        
        # If file is too large for Supabase free tier (>50MB), try to compress more
        if output_size_mb > 45:  # Leave some margin
            logger.warning(f"File size {output_size_mb:.2f} MB may be too large for Supabase free tier")
            # You could implement additional compression here if needed
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        # Clean up any partial output file
        if 'out' in locals() and out:
            out.release()
        if 'cap' in locals() and cap:
            cap.release()
        if 'output_path' in locals() and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise

def test_with_specific_video():
    """
    Test function that processes tennis-forehand-1.mp4 and saves it to tennis-videos-processed
    """
    # Get the current script directory and navigate to the project root
    current_dir = Path(__file__).parent
    project_root = current_dir.parent  # This should be the backend folder
    
    # Define input and output paths
    input_video = project_root / "tennis-videos" / "tennis-forehand-1.mp4"
    output_dir = project_root / "tennis-videos-processed"
    output_video = output_dir / "tennis-forehand-1-processed.mp4"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    if not input_video.exists():
        print(f"❌ Input video not found: {input_video}")
        return
    
    try:
        print(f"🎾 Processing tennis video: {input_video}")
        print(f"📁 Output will be saved to: {output_video}")
        
        # Process the video
        temp_output = process_video(str(input_video))
        
        # Move the temporary file to the desired location
        import shutil
        shutil.move(temp_output, str(output_video))
        
        print(f"✅ Success! Processed video saved to: {output_video}")
        
        # Verify the output
        valid, msg = verify_video(str(output_video))
        print(f"🔍 Verification: {msg}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def verify_video(video_path):
    """
    Verify that a video file is valid and can be played
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Cannot open video"
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Try to read first frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return False, "Cannot read frames"
        
        return True, f"Valid video: {width}x{height}, {fps} fps, {frame_count} frames"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

# Test the processor if run directly
if __name__ == "__main__":
    test_with_specific_video()