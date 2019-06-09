import os
import io
# import the matcher
import re
# import the google cloud client library
from google.cloud import vision
from google.cloud.vision import types

import ALPR as A

def send(imagefile="TR/images/c2.jpg"):
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
    labels = response.text_annotations

    # Extract the text
    textlist = labels[0].description.split("\n")
    print(textlist)

    for i in textlist:
        i = A.formatk(i)
        print(i)
        match = re.match(r"^[\w]{6,7}$", i)
        if match:
            return i

    return "None"


# print(send())

