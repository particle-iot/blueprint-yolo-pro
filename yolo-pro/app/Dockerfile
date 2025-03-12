# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

  # Install system dependencies
  RUN apt-get update && apt-get install -y \
      libsm6 \
      git \
      libxext6 \
      libgl1-mesa-glx \
      libgtk2.0-dev \
      libgtk-3-dev \
      python3-opencv \
      python3-pip && \
      rm -rf /var/lib/apt/lists/*

  # Set permissions for /dev/video0 (V4L2 devices)
  RUN usermod -aG video root

  # Copy the client script
  COPY app-cam.py /app/app-cam.py

  # Copy test images
  COPY test-images /app/test-images

  # Install dependencies
RUN pip install --no-cache-dir opencv-python pillow requests matplotlib scikit-image filterpy

# for now, use particle SDK from git (FIXME after pypy)
RUN pip install --no-cache-dir git+https://github.com/particle-iot/particle-linux-python.git 

# Install SORT tracker dependencies
RUN pip install --no-cache-dir numpy \
    && git clone https://github.com/abewley/sort.git /app/sort \
    && cp /app/sort/sort.py /app/

# Run the client script
CMD ["python", "/app/app-cam.py"]
