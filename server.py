from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    base64_image = request.form['image']
    print(base64_image)
    external_image_id = request.form['externalImageId']
    s3_bucket = request.form['s3Bucket']

    #request jo ki ham bheje ge
    payload = {
        "imgData": base64_image[len("data:image/jpeg;base64,"):]
    }

    # POST request to the API
    api_url = "https://f3huofzqwc6gur3c5b7jx64veq0stzsf.lambda-url.us-east-1.on.aws/"
    response = requests.post(api_url, json=payload)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
