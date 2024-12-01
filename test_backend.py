import requests

# URL of your backend API
url = "http://127.0.0.1:5000/upload"

# Path to the image you want to test with
image_path = "C:\\flask-api\\uploads\\egg.jpg"

# Open the image file
with open(image_path, 'rb') as img_file:
    # Send POST request with the image as form-data
    response = requests.post(url, files={'image': img_file})

# Check the response
if response.status_code == 200:
    print("Response from backend:", response.json())
else:
    print("Error:", response.status_code, response.text)
