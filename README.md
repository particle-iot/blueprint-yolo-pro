# **Particle Blueprint: VLM YOLO Pro - Object Detection**

## **Introduction**
Welcome to the **VLM YOLO Pro Blueprint App** for Particle devices! This project serves as a **starting point** for users looking to integrate **computer vision** into their **Linux-based devices**. It demonstrates **real-time object detection** using **Vision Language Models (VLM) and YOLO Pro** inside a **containerized environment**.

**Use this blueprint to deploy AI-powered vision models on your device!** Follow the steps below to set up, build, and run object detection on your **Tachyon or Raspberry Pi**.

---

## **Project Structure**
This repository supports **Linux-based devices** and is designed for **computer vision inference** using **Python and YOLO Pro**.

```
/particle-vlm-yolo-pro
│── /yolo-pro/          # The VLM YOLO Pro application
│    ├── Dockerfile         # Container setup
│    ├── docker-compose.yaml
│    ├── app/app.py     # Image processing & API calls
│    ├── app/test-images/       # Sample images for inference
│── README.md
```

## **Getting Started: Linux Devices (Tachyon, Raspberry Pi)**
This blueprint runs the **VLM YOLO Pro** app inside a **container** for real-time object detection.

### **1. Set Up Your Particle Linux Device**
Ensure your **Tachyon** or **other supported Linux device** is connected and running.

### **2. Clone & Set Up the Project**
```sh
git clone https://github.com/particle-iot/blueprint-vlm-yolo-pro.git
cd particle-vlm-yolo-pro
```

### **3. Build & Run the Containers**
```sh
docker-compose up --build
```
This will:
- Download the **YOLO Pro model**.
- Start the **inference server**.
- Run the **image processing app**.

### **4. Verify Object Detection**
Once running, the application will:
- **Resize and send images** to the inference API every **10 seconds**.
- Display **detection results in the logs**.

Check the logs:
```sh
docker-compose logs -f app
```

---

## **Contributions**
We welcome contributions to this blueprint! If you'd like to suggest changes, please open a **pull request** in the [VLM YOLO Pro GitHub Repository](https://github.com/particle-iot/blueprint-vlm-yolo-pro).

---

## **Supported Devices**
This blueprint supports:
- **Linux-based devices**, including **Tachyon** and **Raspberry Pi**.

