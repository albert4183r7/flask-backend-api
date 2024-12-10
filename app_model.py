import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load model only once at the start
MODEL_PATH = 'models/model.h5'
model = load_model(MODEL_PATH)

# Preprocess image for model prediction
def preprocess_image(image):
    img = Image.open(image).convert('RGB')
    img = img.resize((128, 128))  # Adjust according to model input size
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Perform prediction
def load_model_and_predict(image):
    img_array = preprocess_image(image)
    
    # Make prediction
    predictions = model.predict(img_array)
    
    # Define class labels
    class_names = ["Mutu 1", "Mutu 2", "Mutu 3"]
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions) * 100

    return predicted_class, confidence
