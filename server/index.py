
from google.cloud import vision

client = vision.ImageAnnotatorClient()
with open('../test_img.png', 'rb') as image_file:
    content = image_file.read()

response = client.logo_detection({
    'content': content,
})

print(response)
