from flask import Flask, request, jsonify
from tensorflow.python.keras.models import load_model

from PIL import Image
import numpy as np

app = Flask(__name__)

# Load your trained ML model
model = load_model('C:\\flask-api\\models\\model.h5')

# Helper function to preprocess image for prediction
def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((224, 224))  # Resize to match model input size
    img_array = np.array(img) / 255.0  # Normalize image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Route to receive image and make a prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Preprocess the image and make prediction
    image = preprocess_image(file)
    predictions = model.predict(image)

    # Assuming model outputs a class index (you may modify depending on your model's output)
    predicted_class = np.argmax(predictions, axis=1)[0]

    # Return the predicted class as a response
    return jsonify({"prediction": str(predicted_class)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
