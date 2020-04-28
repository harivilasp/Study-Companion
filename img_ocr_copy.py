# pip install pillow
from PIL import ImageGrab
import io
import json
import cv2
import numpy as np
import requests
import pyperclip

def printtest():
    img = ImageGrab.grabclipboard()
    # or ImageGrab.grab() to grab the whole screen!
    img.save('screenshot.png','PNG')
    img = cv2.imread("screenshot.png")
    height, width, _ = img.shape
    # Cutting image
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
    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    #print(text_detected)    
    #pyperclip.copy(text_detected)
    #spam = pyperclip.paste()
    return text_detected
