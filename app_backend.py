from flask import Flask, request, jsonify
from app_model import load_model_and_predict

app = Flask(__name__)

@app.route('/')
def index():
    return "Image Classification API is running!"

# Route for image upload and processing
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Perform model prediction
        predicted_class, confidence = load_model_and_predict(file)

        # Return result as JSON
        return jsonify({
            'message': 'File processed successfully',
            'prediction': {
                'predicted_class': predicted_class,
                'confidence': f"{confidence:.2f}%"
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
