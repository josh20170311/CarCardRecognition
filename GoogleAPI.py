import os
import io
# import the matcher
import re
# import the google cloud client library
from google.cloud import vision
from google.cloud.vision import types


def send(imagefile="TR/images/car1.jpg"):
    # instantiates a client
    client = vision.ImageAnnotatorClient()
    # the name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), imagefile)
    # loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # performs label detection on the image file
    response = client.document_text_detection(image=image)
    print(response)
    labels = response.text_annotations
    print(labels)
    # Take out the text
    testlist = labels[0].description.split("\n")
    print('Labels:')
    returnlist = []
    for i in testlist:
        match = re.match(r"^[\w]{2,4}[-, ][\w]{2,4}$", i)
        if match:
            returnlist.append(i)
    if len(returnlist):
        return returnlist[0]
    else:
        return "None"


def test():
    print(send())
