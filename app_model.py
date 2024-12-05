from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import BatchNormalization
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

# Load the model 
model = load_model("models\\model_mobilenetv2.h5")

# Preprocess image
def process_image(img):
    img = Image.fromarray(img).convert('RGB')
    img = img.resize((128,128))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Get model predictions
def get_prediction(img_array):
    predictions = model.predict(img_array)
    class_names = ["Mutu 1", "Mutu 2", "Mutu 3"]
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions) * 100
    return predicted_class, confidence

# Route to receive image and make a prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Process the image
    img = Image.open(file)
    
    max_width = 400
    max_height = 400
    img_width, img_height = img.size
        
    if img_width > max_width or img_height > max_height:
        ratio_width = max_width / float(img_width)
        ratio_height = max_height / float(img_height)
        ratio = min(ratio_width, ratio_height)
        img = img.resize((int(img_width * ratio), int(img_height * ratio)), Image.LANCZOS)
        
    img_array = process_image(np.array(img))

    # Get prediction
    predicted_class, confidence = get_prediction(img_array)
    print(predicted_class, confidence)

    # Return response as JSON
    return jsonify({
        "predicted_class": predicted_class,
        "confidence": confidence
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
