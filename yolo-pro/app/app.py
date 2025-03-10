import time
import requests
import sys
import os
from PIL import Image

# API endpoint
API_URL = "http://inference:1337/api/image"

# Directory containing images
IMAGE_DIR = "/app/test-images"
IMAGE_LIST = [f"cars{i}.png" for i in range(1, 7)]  # cars1.png to cars6.png
TARGET_SIZE = (320, 320)  # Required image size

def resize_image(image_path):
    """Check if the image is the correct size. If not, resize it to 320x320."""
    with Image.open(image_path) as img:
        if img.size != TARGET_SIZE:
            print(f"Resizing {image_path} from {img.size} to {TARGET_SIZE}", flush=True)
            img = img.resize(TARGET_SIZE, Image.LANCZOS)
            img.save(image_path)  # Overwrite with resized version
        else:
            print(f"Skipping resize: {image_path} is already {TARGET_SIZE}", flush=True)
    return image_path

def send_image(image_path):
    """Send an image to the inference API."""
    try:
        with open(image_path, "rb") as img:
            files = {"file": img}
            response = requests.post(API_URL, files=files)

            print(f"Sent {image_path}", flush=True)
            print(f"Response Code: {response.status_code}", flush=True)
            print(f"Response Body: {response.json()}", flush=True)

    except Exception as e:
        print(f"Error sending {image_path}: {e}", flush=True)

def run():
    """Loop through images, resizing if needed, and send them to the API in order."""
    while True:
        time.sleep(10)  # Wait 10 seconds before sending the next request

        for image_name in IMAGE_LIST:
            image_path = os.path.join(IMAGE_DIR, image_name)

            if os.path.exists(image_path):
                resized_path = resize_image(image_path)
                send_image(resized_path)
            else:
                print(f"Image not found: {image_path}, skipping...", flush=True)


if __name__ == "__main__":
    print("Starting the image sender app...", flush=True)
    run()