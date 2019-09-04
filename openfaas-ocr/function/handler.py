try:
    import Image
except ImportError as e:
    from PIL import Image

import ocrmypdf


import io
import pytesseract
import urllib.request
import os
from uuid import uuid4
from urllib.parse import urlparse
from os.path import splitext
import base64
import binascii
import textract


ALLOWED_IMAGE_TYPE = [".jpeg", ".png", ".jpg", ".pdf"]


def get_ext(url):
    parsed = urlparse(url)
    _, ext = splitext(parsed.path)
    return ext


def save_image_from_url(url):
    """Saves image from an URL to local and retruns path"""

    ext = get_ext(url)
    local_file_path = "./tmp/" + str(uuid4()) + ext
    urllib.request.urlretrieve(url, local_file_path)
    return local_file_path


def save_image_from_base64(encoded_string, ext):
    """Saves image to local from base64 encoded string and returns path"""

    local_file_path = "./tmp/" + str(uuid4()) + "." + ext
    with open(local_file_path, "wb") as fh:
        fh.write(base64.decodebytes(bytes(encoded_string, 'utf-8')))
    return local_file_path


def get_image_format(base64_string):
    """returns image format from base64 encoded string"""

    image_stream = io.BytesIO((base64.b64decode(base64_string)))
    image = Image.open(image_stream)
    return image.format


def handle(req):

    decoded = base64.decodebytes(bytes(req, 'utf-8'))
    file_path = save_image_from_base64(req, 'pdf')

    ocrmypdf.ocr(file_path, './tmp/output.pdf', deskew=True)

    text = textract.process('./tmp/output.pdf')

    print(text)
