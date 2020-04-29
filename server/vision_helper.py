import os
import base64
import requests
import json
# import simplejson as json
from google.cloud import vision

TOKEN = os.environ["TOKEN"]
URL = "https://vision.googleapis.com/v1/images:annotate?key={}".format(TOKEN)

# image -> base64 (sent from ios)
def encode_image(image_path):
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode("utf-8")

def image_request(image_path):
	data = {
	  "requests": [
	    {
	      "image": {
	        "content": encode_image(image_path) # "base64-encoded-image"
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
	# data = json.dumps(data)
	# print(data)
	r = requests.post(URL, json=data)
	return r.text
	# return ''

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
	          "type": "LABEL_DETECTION"
	        }
	      ]
	    }
	  ]
	}
	r = requests.post(URL, json=data)
	return r.text


image_path = './resource/test_img.png'
res = json.loads(image_request(image_path))

# error handling
data = res["responses"][0]["textAnnotations"]
word_list = [item["description"] for item in data]
print(word_list)
for word in word_list:
	print(word)


# pics = ['https://i.imgur.com/2EUmDJO.jpg', 'https://i.imgur.com/FPMomNl.png']
# client = vision.ImageAnnotatorClient()
# image = vision.types.Image()

# for pic in pics:
#     image.source.image_uri = pic
#     response = client.label_detection(image=image)	
#     labels = response.label_annotations
#     print("'Labels: ")
#     for label in labels:
#     	print(label.description)

    # print('=' * 79)
    # print('File: {pic}')
    # print
    # for face in response.face_annotations:
    # 	print(face)
    	# likelihood = vision.enums.Likelihood(face.surprise_likelihood)
    	# vertices = [f'({v.x},{v.y})' for v in face.bounding_poly.vertices]
        # print(f'Face surprised: {likelihood.name}')
        # print(f'Face bounds: {",".join(vertices)}')
