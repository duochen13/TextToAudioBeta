
from google.cloud import vision

pics = ['https://i.imgur.com/2EUmDJO.jpg', 'https://i.imgur.com/FPMomNl.png']
client = vision.ImageAnnotatorClient()
image = vision.types.Image()

for pic in pics:
    image.source.image_uri = pic
    response = client.label_detection(image=image)	
    labels = response.label_annotations
    print("'Labels: ")
    for label in labels:
    	print(label.description)


    # print('=' * 79)
    # print('File: {pic}')
    # print
    # for face in response.face_annotations:
    # 	print(face)
    	# likelihood = vision.enums.Likelihood(face.surprise_likelihood)
    	# vertices = [f'({v.x},{v.y})' for v in face.bounding_poly.vertices]
        # print(f'Face surprised: {likelihood.name}')
        # print(f'Face bounds: {",".join(vertices)}')
