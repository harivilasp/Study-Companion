# pip install pillow
from PIL import Image
import io
import json
import cv2
import numpy as np
import requests

def ocr_from_imagefile(file_storage, api_key=None):
    """
    Accepts a Flask FileStorage object or file-like object, sends to OCR.space, returns detected text.
    """
    url_api = "https://api.ocr.space/parse/image"
    if api_key is None:
        # Try to load from .env or fallback to demo key
        import os
        api_key = os.getenv("OCR_API_KEY")
    # Read image bytes
    file_bytes = file_storage.read()
    file_storage.seek(0)  # Reset pointer for Flask reuse
    result = requests.post(url_api,
                  files = {"image.jpg": file_bytes},
                  data = {"apikey": api_key,
                          "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)
    parsed_results = result.get("ParsedResults", [{}])[0]
    text_detected = parsed_results.get("ParsedText", "")
    return text_detected

# Legacy function for clipboard screenshots remains for backward compatibility
from PIL import ImageGrab
import pyperclip

def printtest():
    img = ImageGrab.grabclipboard()
    img.save('screenshot.png','PNG')
    img = cv2.imread("screenshot.png")
    height, width, _ = img.shape
    roi = img[0: height, 0: width]
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)
    result = requests.post(url_api,
                  files = {"screenshot.jpg": file_bytes},
                  data = {"apikey": "28578780c488957",
                          "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)
    parsed_results = result.get("ParsedResults", [{}])[0]
    text_detected = parsed_results.get("ParsedText", "")
    return text_detected
