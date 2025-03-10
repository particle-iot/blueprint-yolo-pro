# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy the client script
COPY app-cam.py /app/app-cam.py
COPY app-video.py /app/app-video.py

# Copy test images
COPY test-images /app/test-images

# Install dependencies
RUN pip install --no-cache-dir opencv-python-headless pillow requests matplotlib scikit-image filterpy

# Install SORT tracker dependencies
RUN pip install --no-cache-dir numpy \
    && git clone https://github.com/abewley/sort.git /app/sort \
    && cp /app/sort/sort.py /app/

# Run the client script
CMD ["python", "/app/app-video.py"]
