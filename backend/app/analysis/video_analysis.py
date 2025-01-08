from flask import Flask, request, jsonify
import cv2
import os
import mediapipe as mp

app = Flask(__name__)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

@app.route('/analyze', methods=['POST'])
def analyze_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join('/tmp', filename)
    file.save(filepath)

    # Perform analysis
    cap = cv2.VideoCapture(filepath)
    frame_count = 0
    feedback = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame with MediaPipe
        frame_count += 1
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Example feedback based on pose detection
        if results.pose_landmarks:
            feedback.append(f"Frame {frame_count}: Pose detected")
        else:
            feedback.append(f"Frame {frame_count}: No pose detected")

    cap.release()
    os.remove(filepath)  # Clean up the temporary file

    return jsonify({"message": "Analysis completed", "feedback": feedback})
