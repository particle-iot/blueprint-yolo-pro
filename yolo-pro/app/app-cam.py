import cv2
import time
import requests
import os
import signal
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from sort import Sort  # Import SORT tracker

# Constants
API_URL = "http://inference:1337/api/image"
TARGET_SIZE = (320, 320)  # Target image size
OUTPUT_DIR = "/app/output"  # Directory for processed frames
VIDEO_FILE = os.getenv("VIDEO_FILE", "/dev/video2")  # Default to first V4L2 camera
OUTPUT_VIDEO_PATH = os.path.join(OUTPUT_DIR, "output-annotate.mp4")  # MP4 output path
FRAME_RATE = 30  # Frames per second for the output video

DISPLAY_FRAMES = os.getenv("DISPLAY_FRAMES", "0") == "1"
DISPLAY_AVAILABLE = "DISPLAY" in os.environ and os.environ["DISPLAY"]

if DISPLAY_FRAMES and DISPLAY_AVAILABLE:
    print("✅ GUI display is available. Frames will be shown.")
else:
    print("⚠️ No GUI display detected. Running headless.")

# Ensure output directory exists inside the container
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global variable for video writer
video_writer = None
car_tracker = Sort()  # Initialize SORT tracker
unique_car_ids = set()  # Store unique car IDs

car_id_map = {}  # Dictionary to store custom car IDs
next_car_id = 1  # Start from ID 1

def resize_image(frame):
    """Resize the frame to 320x320."""
    img = Image.fromarray(frame)
    img = img.resize(TARGET_SIZE, Image.LANCZOS)
    return img

def send_image(image):
    """Send an image to the inference API and return the response."""
    try:
        image_path = "/tmp/captured_frame.png"
        image.save(image_path)  # Save temp file

        with open(image_path, "rb") as img:
            files = {"file": img}
            response = requests.post(API_URL, files=files, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            print(f"Response Body: {response_data}", flush=True)
            return response_data
        else:
            print(f"Error: Received response code {response.status_code}", flush=True)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error sending frame: {e}", flush=True)
        return None

def draw_bounding_boxes(image, response):
    """Draw bounding boxes on the image based on API response."""
    global next_car_id, car_id_map
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    detections = []

    if "result" in response and "bounding_boxes" in response["result"]:
        for box in response["result"]["bounding_boxes"]:
            x, y, width, height = box["x"], box["y"], box["width"], box["height"]
            detections.append([x, y, x + width, y + height, 1.0])  # Format correctly

    detections = np.array(detections)
    if detections.shape[0] == 0:
        detections = np.empty((0, 5))
    
    tracked_objects = car_tracker.update(detections)
    
    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = obj
        obj_id = int(obj_id)
        if obj_id not in unique_car_ids:
            unique_car_ids.add(obj_id)
            car_id_map[obj_id] = next_car_id
            next_car_id += 1
            print(f"New car detected: ID {obj_id} - now seen {len(unique_car_ids)} using id {car_id_map[obj_id]}", flush=True)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 10), f"Vehicle: {car_id_map[obj_id]}", font=font, fill="red")
    
    return image

def setup_video_writer(frame_width, frame_height):
    """Initialize the video writer."""
    global video_writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    video_writer = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, FRAME_RATE, (frame_width, frame_height))
    print(f"Initialized video writer at {OUTPUT_VIDEO_PATH}", flush=True)

def close_video_writer():
    """Ensure the video file is properly closed."""
    global video_writer
    if video_writer is not None:
        video_writer.release()
        print(f"Video file saved at {OUTPUT_VIDEO_PATH}", flush=True)
    video_writer = None

def process_video():
    """Read frames from the V4L2 camera, send them to inference API, and save results."""
    global video_writer

    cap = cv2.VideoCapture(VIDEO_FILE)
    if not cap.isOpened():
        print(f"ERROR: Unable to open video source {VIDEO_FILE}", flush=True)
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    setup_video_writer(TARGET_SIZE[0], TARGET_SIZE[1] )

    print("frame_width {frame_width} frame_height {frame_height}", flush=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.", flush=True)
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        image = resize_image(frame_rgb)  # Resize to 320x320

        response = send_image(image)
        if response is None:
            continue

        image_with_boxes = draw_bounding_boxes(image, response)
        frame_with_boxes = cv2.cvtColor(np.array(image_with_boxes), cv2.COLOR_RGB2BGR)

        if video_writer is not None:
            video_writer.write(frame_with_boxes)

        if DISPLAY_FRAMES and DISPLAY_AVAILABLE:
            cv2.imshow("Live Video", frame_with_boxes)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    close_video_writer()
    if DISPLAY_FRAMES:
        cv2.destroyAllWindows()
    print("Finished processing video.", flush=True)

def main():
    """Start processing the video file or V4L2 camera."""
    print("Starting video processing...", flush=True)
    process_video()

if __name__ == "__main__":
    main()
