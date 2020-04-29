import os
import requests
import json
from flask import Flask, request, jsonify
from google.cloud import vision

TOKEN = os.environ["TOKEN"]
URL = "https://vision.googleapis.com/v1/images:annotate?key={}".format(TOKEN)


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        image_base_content = request.json['content']
        print("\nreceived image, processing...")
        vision_result = get_vision_result(image_base_content)
        print("\nvision result:\n {}".format(vision_result))
        # paring response, error handling to be added
        labels = json.loads(vision_result)["responses"][0]["labelAnnotations"]
        response = [label["description"] for label in labels]
        # labels: [l1, l2, l3, l4]
    return jsonify(labels=response)

# helper function
def get_vision_result(image_base_content):
    data = {
      "requests": [
        {
          "image": {
            "content": image_base_content # "base64-encoded-image"
          },
          "features": [
            {
              "maxResults": 5,
              "type": "DOCUMENT_TEXT_DETECTION" # "LABEL_DETECTION"
            }
          ]
        }
      ]
    }
    r = requests.post(URL, json=data)
    return r.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
