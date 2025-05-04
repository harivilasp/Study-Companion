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
    Handles unexpected responses gracefully.
    """
    import logging
    logger = logging.getLogger(__name__)

    url_api = "https://api.ocr.space/parse/image"
    if api_key is None:
        import os
        api_key = os.getenv("OCR_API_KEY")
    file_bytes = file_storage.read()
    file_storage.seek(0)
    try:
        response = requests.post(url_api,
                  files = {"image.jpg": file_bytes},
                  data = {"apikey": api_key,
                          "language": "eng"})
        response_text = response.content.decode()
        try:
            result = json.loads(response_text)
        except Exception as e:
            logger.error(f"OCR API did not return JSON: {response_text}")
            return f"OCR API error: {response_text}"
        if not isinstance(result, dict):
            logger.error(f"OCR API returned non-dict: {result}")
            return f"OCR API error: {result}"
        parsed_results = result.get("ParsedResults")
        if not parsed_results or not isinstance(parsed_results, list) or not parsed_results[0]:
            logger.error(f"OCR API missing ParsedResults: {result}")
            return f"OCR API error: {result.get('ErrorMessage', 'No text found / OCR failed.')}"
        text_detected = parsed_results[0].get("ParsedText", "")
        return text_detected
    except Exception as e:
        logger.error(f"Exception in OCR: {e}")
        return f"OCR error: {str(e)}"

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
