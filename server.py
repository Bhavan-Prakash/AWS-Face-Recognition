import cv2
import numpy as np
import base64
import boto3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Initialize AWS Rekognition client
rekognition = boto3.client('rekognition')

@app.route('/')
def index():
    return render_template('index.html')

def recognize_face(image_bytes):
    # Rekognition API parameters
    params = {
        'CollectionId': 'faces-collection',
        'FaceMatchThreshold': 90,
        'Image': {'Bytes': image_bytes},
        'MaxFaces': 5
    }

    # Call Rekognition
    response = rekognition.search_faces_by_image(**params)

    return response

def check_image_availability(base64_image):
    # Convert base64 image data to bytes
    image_bytes = base64.b64decode(base64_image)

    # Convert bytes to OpenCV image format
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # List all objects (images) in the S3 bucket
    s3_params = {
        'Bucket': 'testing-bhavan'
    }

    s3_objects = s3.list_objects_v2(**s3_params)
    image_keys = [obj['Key'] for obj in s3_objects.get('Contents', [])]

    # Iterate over each image in the bucket and perform recognition
    match_found = False
    for image_key in image_keys:
        # Rekognition recognition for the current image
        recognition_result = recognize_face(image_bytes)

        if recognition_result.get('FaceMatches'):
            match_found = True
            return {'match_found': match_found, 'message': 'Face recognized successfully', 'name': image_key}

    return {'match_found': match_found, 'message': 'Face not recognized'}

@app.route('/upload', methods=['POST'])
def upload_image():
    base64_image = request.json.get('image')

    if not base64_image:
        return jsonify({'error': 'Image data not provided'}), 400

    # Check the availability of the image in the S3 bucket and recognize the face
    response_data = check_image_availability(base64_image)

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)






# import cv2
# import numpy as np
# import base64
# import boto3
# from flask import Flask, request, jsonify, render_template

# app = Flask(__name__)

# # Initialize AWS Rekognition client
# rekognition = boto3.client('rekognition')

# # Initialize AWS S3 client
# s3 = boto3.client('s3')

# @app.route('/')
# def index():
#     return render_template('index.html')

# def recognize_face(image_bytes):
#     # Rekognition API parameters
#     params = {
#         'CollectionId': 'faces-collection',
#         'FaceMatchThreshold': 90,
#         'Image': {'Bytes': image_bytes},
#         'MaxFaces': 5
#     }

#     # Call Rekognition
#     response = rekognition.search_faces_by_image(**params)

#     return response

# def encode_image_to_base64(image):
#     _, buffer = cv2.imencode('.jpg', image)
#     return base64.b64encode(buffer).decode('utf-8')

# def check_image_availability(image):
#     # Convert image to base64 format
#     base64_image = encode_image_to_base64(image)

#     # List all objects (images) in the S3 bucket
#     s3_params = {
#         'Bucket': 'testing-bhavan'
#     }

#     s3_objects = s3.list_objects_v2(**s3_params)
#     image_keys = [obj['Key'] for obj in s3_objects.get('Contents', [])]

#     # Iterate over each image in the bucket and perform recognition
#     match_found = False
#     for image_key in image_keys:
#         # Rekognition recognition for the current image
#         recognition_result = recognize_face(image)

#         if recognition_result.get('FaceMatches'):
#             match_found = True
#             return {'match_found': match_found, 'message': 'Face recognized successfully', 'name': image_key}

#     return {'match_found': match_found, 'message': 'Face not recognized'}

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     # Get the image data from the request
#     request_body = request.json

#     if not request_body or 'imgData' not in request_body.get('body', {}):
#         return jsonify({'error': 'Invalid request body format or missing image data'}), 400

#     img_data = request_body['body']['imgData']

#     # Decode base64 image data to bytes
#     image_bytes = base64.b64decode(img_data)

#     # Convert bytes to OpenCV image format
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Check the availability of the image in the S3 bucket and recognize the face
#     result = check_image_availability(image)

#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(debug=True)




# import boto3
# from botocore.exceptions import ClientError
# from flask import Flask, request, jsonify, render_template

# app = Flask(__name__)

# # Initialize AWS S3 client
# s3 = boto3.client('s3')

# @app.route('/')
# def index():
#     return render_template('index.html')

# def check_image_availability(base64_image):
    
#     # Implement your logic to check the availability of the image in the S3 bucket
#     # For demonstration, let's not set the initial value of match_found
#     response_data = {}

#     # Your actual logic here to determine if the image is found in the S3 bucket
#     # For demonstration purposes, let's assume the image is found
#     if some_logic_to_check_availability(base64_image):
#         response_data['match_found'] = True
#         response_data['message'] = 'Match found'
#     else:
#         response_data['match_found'] = False
#         response_data['message'] = 'Not found'

#     return response_data

# def some_logic_to_check_availability(base64_image):
#     # Your actual logic here to check the availability of the image in the S3 bucket
#     # This could involve listing objects in the bucket and comparing the images
#     # For demonstration purposes, let's return True
#     return True

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     base64_image = request.json.get('image')

#     if not base64_image:
#         return jsonify({'error': 'Image data not provided'}), 400

#     # Check the availability of the image in the S3 bucket
#     response_data = check_image_availability(base64_image)

#     return jsonify(response_data)

# if __name__ == "__main__":
#     app.run(debug=True)






# import boto3
# from botocore.exceptions import ClientError
# from flask import Flask, request, jsonify, render_template

# app = Flask(__name__)

# # Initialize AWS S3 client
# s3 = boto3.client('s3')

# @app.route('/')
# def index():
#     return render_template('index.html')

# def check_image_availability(base64_image):
#     # Implement your logic to check the availability of the image in the S3 bucket
#     # For demonstration, let's assume the image is not found
#     match_found = False

#     # Example response
#     response_data = {'match_found': match_found}

#     if match_found:
#         response_data['message'] = 'Match found'
#     else:
#         response_data['message'] = 'Not found'

#     return response_data

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     base64_image = request.json.get('image')

#     if not base64_image:
#         return jsonify({'error': 'Image data not provided'}), 400

#     # Check the availability of the image in the S3 bucket
#     response_data = check_image_availability(base64_image)

#     return jsonify(response_data)

# if __name__ == "__main__":
#     app.run(debug=True)
















# from flask import Flask, request, jsonify, render_template
# import cv2
# import numpy as np
# import base64
# import boto3

# app = Flask(__name__)

# # Initialize AWS S3 client
# s3 = boto3.client('s3')

# @app.route('/')
# def index():
#     return render_template('index.html')

# def capture_webcam_image():
#     # Open webcam
#     cap = cv2.VideoCapture(0)

#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Release the capture
#     cap.release()

#     return frame

# def encode_image_to_base64(image):
#     _, buffer = cv2.imencode('.jpg', image)
#     return base64.b64encode(buffer).decode('utf-8')

# def search_image_in_s3(base64_image):
#     # Decode base64 image
#     image = base64.b64decode(base64_image)

#     # Here, you'd implement your logic to compare the image with images in the S3 bucket
#     # For simplicity, let's assume we're checking for a specific file in the bucket

#     # Check if the image exists in the S3 bucket
#     bucket_name = 'testing-bhavan'
#     image_key = 'webcam_image.jpg'  # Example image key
#     try:
#         s3.head_object(Bucket=bucket_name, Key=image_key)
#         match_found = True
#     except Exception as e:
#         match_found = False

#     return {'match_found': match_found}

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     # Get JSON input
#     request_data = request.json

#     # Extract image data from JSON
#     img_data = request_data.get('body', {}).get('imgData', '')

#     # Search for image in S3 bucket
#     search_result = search_image_in_s3(img_data)

#     # Return JSON response with search result
#     return jsonify(search_result)

# if __name__ == "__main__":
#     app.run(debug=True)


















#ishav bhai code of adding picture to s3 using api
# from flask import Flask, request, jsonify, render_template
# import requests
# import base64

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     base64_image = request.form['image']

#     # Construct the request payload
#     payload = {
#         "imgData": base64_image,
#         "externalImageId": "bhavan",
#         "s3Bucket": "testing-bhavan"
#     }

#     # Send POST request to the API
#     api_url = "https://36xeylfygqapv45fgldb2ibsp40qrvpb.lambda-url.us-east-1.on.aws/"
#     response = requests.post(api_url, json=payload)

#     return jsonify(response.json())

# if __name__ == "__main__":
#     app.run(debug=True)
 