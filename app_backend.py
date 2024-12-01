import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

# Local directory for storing uploaded images (instead of Cloud Storage for now)
UPLOAD_FOLDER = 'storage/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload an image and send it to the model inference API
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the image locally
        file.save(file_path)

        # Send the image path to model API for classification
        result = send_to_model_api(file_path)
        return jsonify({"classification_result": result}), 201
    else:
        return jsonify({"error": "Invalid file type"}), 400

# Function to send image path to model inference API
def send_to_model_api(image_path):
    model_api_url = "http://127.0.0.1:5001/predict"  # URL for the model inference API

    # Open image and send to model API
    with open(image_path, 'rb') as img_file:
        files = {'image': (image_path, img_file)}
        response = requests.post(model_api_url, files=files)

    if response.status_code == 200:
        return response.json().get("prediction", "No prediction")
    else:
        return "Error in prediction"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
