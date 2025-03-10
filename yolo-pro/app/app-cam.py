import cv2
import time
import requests
import os
import threading
from PIL import Image

# API endpoint
API_URL = "http://inference:1337/api/image"
TARGET_SIZE = (320, 320)  # Target image size
CHECK_INTERVAL = 5  # Time to wait before checking for a new camera

def resize_image(frame):
    """Resize the frame to 320x320."""
    img = Image.fromarray(frame)
    img = img.resize(TARGET_SIZE, Image.LANCZOS)
    return img

def send_image(image):
    """Send an image to the inference API."""
    try:
        image_path = "/tmp/captured_frame.png"
        image.save(image_path)  # Save temp file

        with open(image_path, "rb") as img:
            files = {"file": img}
            response = requests.post(API_URL, files=files)

        print(f"Sent frame, Response Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
    except Exception as e:
        print(f"Error sending frame: {e}")

def get_available_camera():
    """Try to find an available webcam by checking multiple indexes."""
    for index in range(5):  # Check first 5 possible camera indexes
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cap.release()
            return index
    return None

def capture_and_send():
    """Capture frames from the first available webcam and send them as fast as possible."""
    while True:
        cam_index = get_available_camera()
        if cam_index is None:
            print("No webcam found, waiting...")
            time.sleep(CHECK_INTERVAL)
            continue

        print(f"Webcam detected at index {cam_index}, starting capture...")
        cap = cv2.VideoCapture(cam_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame, retrying...")
                time.sleep(1)
                break

            # Resize frame to target size
            image = resize_image(frame)
            send_image(image)

        cap.release()
        print("Webcam disconnected, stopping capture...")
        time.sleep(CHECK_INTERVAL)  # Wait before checking for new camera

def main():
    """Start monitoring for webcams and capturing frames."""
    print("Starting webcam detection...")
    capture_and_send()

if __name__ == "__main__":
    main()