# script use to test the API, can also use postman!

import requests

# Backend API URL (replace with your actual backend API URL)
url = "http://<vm-external-ip>:5000/upload"  

# Path to test image
image_path = "uploads/test_image.jpg"

# Simulate sending a request with an image to the backend
def test_upload_image():
    try:
        # Open the image file
        with open(image_path, 'rb') as img_file:
            # Prepare the payload for the POST request (file upload)
            files = {'file': img_file}
            
            # Send the request to the backend
            response = requests.post(url, files=files)
            
            # Print response from the backend
            if response.status_code == 200:
                print("API call successful.")
                print("Response JSON:", response.json())
            else:
                print(f"Failed to call API. Status Code: {response.status_code}")
                print("Response Text:", response.text)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Run the test function
    test_upload_image()
