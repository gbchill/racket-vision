from flask import Blueprint, request, jsonify
import os

bp = Blueprint('main', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')  # Get the uploaded file
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Define a directory to save the file temporarily
    temp_dir = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # Create the 'temp' directory if it doesn't exist

    # Save the uploaded file
    save_path = os.path.join(temp_dir, file.filename)
    file.save(save_path)

    # Respond with the saved file path (for debugging)
    return jsonify({"message": f"Video saved to {save_path}"})
