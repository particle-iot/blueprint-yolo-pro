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
VIDEO_FILE = "/app/test-images/vehicle-bridge.mp4"  # Path to the video file
OUTPUT_DIR = "/app/output"  # Directory for processed frames
OUTPUT_VIDEO_PATH = os.path.join(OUTPUT_DIR, "vehicle-bridge-annotate.mp4")  # MP4 output path
IMAGE_OUTPUT = False  # Set to True to save individual frames as images
FRAME_RATE = 30  # Frames per second for the output video

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

        # print(f"Sent frame, Response Code: {response.status_code}", flush=True)

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

            #add to car_id_map and assign it the incremented next_car_id
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

def handle_exit(signum, frame):
    """Gracefully handle program exit (including Docker termination)."""
    print("Terminating process, ensuring video is saved...", flush=True)
    close_video_writer()

    # print how many cars were detected
    print(f"Total number of unique cars detected: {len(unique_car_ids)}", flush=True)

    exit(0)

# Attach signal handlers to ensure clean shutdown
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def process_video():
    """Read frames from the video file, send them to inference API, and save results."""
    global video_writer

    cap = cv2.VideoCapture(VIDEO_FILE)
    if not cap.isOpened():
        print(f"ERROR: Unable to open video file {VIDEO_FILE}", flush=True)
        return

    frame_count = 0
    print("Processing video...", flush=True)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    setup_video_writer(TARGET_SIZE[0], TARGET_SIZE[1])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.", flush=True)
            break

        frame_count += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        image = resize_image(frame_rgb)  # Resize to 320x320

        # Send frame to API and get response
        #time how long it took
        start = time.time()
        response = send_image(image)
        end = time.time()
        print(f"Time taken to send image: {end - start} seconds", flush=True)

        if response is None:
            print("Skipping frame due to API failure.", flush=True)
            continue

        # Draw bounding boxes on the frame
        image_with_boxes = draw_bounding_boxes(image, response)

        # Convert PIL image back to OpenCV format for video writing
        frame_with_boxes = cv2.cvtColor(np.array(image_with_boxes), cv2.COLOR_RGB2BGR)

        # Write to video
        if video_writer is not None:
            video_writer.write(frame_with_boxes)

        # Save individual frames (if enabled)
        if IMAGE_OUTPUT:
            output_path = os.path.join(OUTPUT_DIR, f"frame_{frame_count:04d}.jpg")
            image_with_boxes.save(output_path)
            print(f"Saved frame to: {output_path}", flush=True)

        # Debugging: List output directory contents
        # list_output_files()

        # Small delay (avoid spamming API)
        # time.sleep(0.1)

    cap.release()
    close_video_writer()
    print("Finished processing video.", flush=True)

def main():
    """Start processing the video file."""
    print("Starting video processing...", flush=True)
    process_video()

if __name__ == "__main__":
    main()