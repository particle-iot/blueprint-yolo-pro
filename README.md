# **Particle Blueprint: YOLO Pro - Object Detection**

## **Getting Started: Do This First**

Welcome to the **YOLO Pro Blueprint App** for **Particle Tachyon**! This is one of **Particle's Blueprints**, leveraging **container technology** to bundle together models and applications into a **consistent framework**. These apps can run on various platforms without requiring deep platform knowledge.

### **What This Blueprint Does**
1. **Runs Edge Impulse's YOLO Pro model** – an **early beta** designed for traffic analysis, garage monitoring, and other vision-based applications.
2. **Integrated with Particle's platform** – Apps can be pushed **over-the-air** to fleets of devices, **or** run locally for development and testing.
3. **Identical Execution** – Whether deployed **remotely** or **run locally**, the application behaves the same.
4. **Dynamic Display Support** – If a display is **available**, detected objects are shown visually. Otherwise, results are logged.
5. **Cloud Reporting** – The application can send detections to the cloud (requires **Wi-Fi, Ethernet, or Cellular** connectivity).
6. **Visual Studio Code has Particle's Workbench plugin already installed** – This handles starting, stopping, and pushing containers to the cloud.
7. **Device is already logged into your account** – This happens during setup. If you're using a **device pre-setup from our factory**, no additional login is needed.

This blueprint is available free and open source on our github platform. 

---

### **Run This App in Three Easy Steps**

#### **1. Connect Your Hardware**
- Plug in your **webcam** to the **USB-C host port** on the **Tachyon**.

#### **2. Open the Visual Studio Code Command Palette**
- Press **Ctrl + Shift + P** (or **Cmd + Shift + P** on Mac).
- Type `Particle App Run`.
- Select `Particle App Run` from the list.

#### **3. Run the App**
- The container will build and execute locally.
- The webcam feed will appear on-screen.
- Use the **included test card** to detect and verify object recognition.

#### **4. View Results in the Cloud**
Once running, you can view real-time detection events in the cloud:
[Cloud Event Dashboard](your-cloud-event-link-here)

#### **5. Stop the app**
Press control-c in the console and it will stop!
Run it again if you want :)

**Note:** Ensure your device has an active **Wi-Fi, Ethernet, or Cellular** connection to report events.

---

## **Project Structure**
This repository is designed for **computer vision inference** using **Python and YOLO Pro** inside a container.

```
/particle-vlm-yolo-pro
│── /yolo-pro/          # The VLM YOLO Pro application
│    ├── Dockerfile         # Container setup
│    ├── docker-compose.yaml
│    ├── app/app.py     # Image processing & API calls
│    ├── app/test-images/       # Sample images for inference
│── README.md
```

---

## **Contributions**
We welcome contributions to this blueprint! If you'd like to suggest changes, please open a **pull request** in the [VLM YOLO Pro GitHub Repository](https://github.com/particle-iot/blueprint-vlm-yolo-pro).

---

## **Supported Devices**
This blueprint supports:
- **Particle Tachyon**
- **Other Linux-based devices (e.g., Raspberry Pi)**

