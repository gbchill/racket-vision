import os
import cv2
import mediapipe as mp
import subprocess

def process_video_with_mediapipe(input_path, output_folder):
    """
    Process a video with MediaPipe to overlay pose skeletons, save the result, 
    and re-encode it to a browser-compatible format (H.264).

    Args:
        input_path (str): Path to the input video file.
        output_folder (str): Folder to save the processed video.

    Returns:
        str: Path to the final re-encoded video file.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Extract the input file name and prepare the intermediate and final output paths
    file_name = os.path.basename(input_path)
    intermediate_output_path = os.path.join(output_folder, f"mediapipe_{file_name}")
    final_output_path = os.path.join(output_folder, f"mediapipe-processed-h264_{file_name}")

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    # Open the input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video file: {input_path}")

    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for the intermediate video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize the VideoWriter for intermediate processing
    out = cv2.VideoWriter(intermediate_output_path, fourcc, fps, (width, height))

    print(f"Processing video: {input_path}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        results = pose.process(rgb_frame)

        # Draw pose landmarks and connections on the frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # Original BGR frame for drawing
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )

        # Write the processed frame to the intermediate video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    print(f"Intermediate video saved to: {intermediate_output_path}")

    # Re-encode the intermediate video to H.264 for browser compatibility
    reencode_command = [
        "ffmpeg", "-i", intermediate_output_path,
        "-vcodec", "libx264", "-acodec", "aac", "-strict", "experimental",
        final_output_path
    ]

    try:
        subprocess.run(reencode_command, check=True)
        print(f"Final re-encoded video saved to: {final_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during video re-encoding: {e}")
        raise

    # Return the path to the final re-encoded video
    return final_output_path

# Example test script
if __name__ == "__main__":
    # Input video path from the temp folder
    input_video = "temp/forehand-shot.mp4"
    
    # Create a new folder for output videos
    output_dir = "output"
    
    try:
        result_path = process_video_with_mediapipe(input_video, output_dir)
        print(f"MediaPipe processed video created at: {result_path}")
    except Exception as e:
        print(f"Error processing video: {e}")
