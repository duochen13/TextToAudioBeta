from flask import Flask, request
from google.cloud import vision
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        image_base_content = request.json['content']
        print(image_base_content)
        # print(request.json['request'])
    return 'this is test'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

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
