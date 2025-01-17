import sys
import os
from flask import Flask, send_from_directory
from flask_cors import CORS  # Import CORS
from app.routes import routes  # Adjusted import since routes is in app/

# Add the backend directory to Python's module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Limit file upload size to 500 MB
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB

# Register the blueprint
app.register_blueprint(routes)

# Serve the output folder
@app.route("/output/<path:filename>")
def serve_output_file(filename):
    return send_from_directory("output", filename, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)
