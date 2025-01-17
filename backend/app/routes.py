import os
import logging
from flask import Blueprint, request, jsonify, send_from_directory
from app.analysis.video_analysis import process_video_with_mediapipe

routes = Blueprint("routes", __name__)

# Path to the temporary and output folders
TEMP_FOLDER = "temp"
OUTPUT_FOLDER = "output"

# Setup logging
logging.basicConfig(level=logging.INFO)

@routes.route("/analyze", methods=["POST"])
def analyze_video():
    if "file" not in request.files:
        logging.error("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        # Save uploaded video to TEMP_FOLDER
        os.makedirs(TEMP_FOLDER, exist_ok=True)
        input_path = os.path.join(TEMP_FOLDER, file.filename)
        file.save(input_path)
        logging.info(f"Uploaded file saved to: {input_path}")

        # Process video
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        output_path = process_video_with_mediapipe(input_path, OUTPUT_FOLDER)
        logging.info(f"Processed video saved to: {output_path}")

        if not os.path.exists(output_path):
            logging.error("Processed video file not found")
            return jsonify({"error": "Failed to process video"}), 500

        # Return re-encoded video path
        return jsonify({"output_path": f"/output/{os.path.basename(output_path)}"})

    except Exception as e:
        logging.error(f"Error processing video: {str(e)}")
        return jsonify({"error": "An error occurred during processing"}), 500
