import os
import io
#imaport the google cloud client library
from google.cloud import vision
from google.cloud.vision import types
#instantiates a client
client = vision.ImageAnnotatorClient()
#the name of the image file to annotate
file_name = os.path.join(os.path.dirname(__file__),'TR\\images\\TaiwanStreet.jpg')
#loads the image into memory
with io.open(file_name,'rb') as image_file :
    content = image_file.read()

image = types.Image(content = content)

#performs label dtection on the image file
response = client.text_detection(image = image)
print(response)
#labels = response.text_annotations
#print('Labels:')
#for label in labels:
#    print(label.description)