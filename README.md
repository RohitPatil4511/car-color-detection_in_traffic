# 🚗🚦 Car Colour Detection in Traffic using YOLOv8

> 🔥 Smart Computer Vision System for Real-Time Traffic Analysis

---

## 🌟 Overview

An advanced **Computer Vision project** that detects **cars and people in traffic scenes**, identifies **blue-colored cars**, and provides **real-time analytics** using **YOLOv8 + OpenCV**.

This system is designed for **smart traffic monitoring**, **urban analytics**, and **AI-based surveillance systems**.

---

## 🎯 Key Features

✨ **Vehicle Detection**

* Detects **cars only** (filters out trucks, buses, bikes)

✨ **Color Intelligence**

* Identifies **blue cars** using HSV color detection

✨ **People Detection**

* Counts pedestrians at traffic signals

✨ **Smart Visualization**

* 🔴 Red Box → Blue Cars
* 🔵 Blue Box → Other Cars
* 🟢 Green Box → People

✨ **Live Counters**

* 🚗 Total Cars
* 🔴 Blue Cars
* 🔵 Other Cars
* 👤 People Count

✨ **User-Friendly GUI**

* Built using **Tkinter**
* Supports:

  * 📷 Image Upload
  * 🎥 Video Upload
  * 📹 Live Webcam Detection

---

## 🧠 How It Works

1. YOLOv8 detects objects in each frame
2. Filters only **car** and **person** classes
3. Extracts car region for color analysis
4. Applies **HSV color detection**
5. Classifies:

   * Blue Car → 🔴 Red Box
   * Other Car → 🔵 Blue Box
   * Person → 🟢 Green Box
6. Displays real-time counts on screen

---

## 🏗️ Project Structure

```
car_colour_detection_project/
│── app.py                # GUI application
│── detector.py           # YOLOv8 detection logic
│── color_classifier.py   # Color detection logic
│── requirements.txt
│── README.md
│── .gitignore
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/RohitPatil4511/car-color-detection_in_traffic.git
cd car-color-detection_in_traffic
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```
python app.py
```

---

## 📦 Requirements

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* NumPy
* Pillow
* Tkinter

---

## 📊 Output Example

✔️ Real-time bounding boxes
✔️ Smart color classification
✔️ Live counters displayed on screen

---

## 🚀 Use Cases

* 🚦 Smart Traffic Signal Monitoring
* 🏙️ Smart City Applications
* 🚗 Vehicle Color-Based Filtering
* 👥 Crowd Detection at Signals
* 🎓 Academic AI/ML Projects

---

## ⚠️ Notes

* 🌞 Works best in **daylight conditions**
* ⚠️ White/silver cars may reflect sky color
* 📥 YOLO model (`yolov8n.pt`) auto-downloads on first run

---

## 🔥 Future Improvements

* 🎯 Improve color detection with Deep Learning
* 🚗 Multi-color classification (Red, Black, White, etc.)
* 📊 Dashboard with analytics graphs
* ☁️ Deploy as web app (Streamlit/Flask)

---

## 👨‍💻 Author

**Rohit Patil**
🔗 GitHub: https://github.com/RohitPatil4511

---

## ⭐ Support

If you like this project:
👉 Give it a **⭐ on GitHub**
👉 Share with your friends 🚀

---
