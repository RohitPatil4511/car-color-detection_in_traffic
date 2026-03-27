# Car Colour Detection in Traffic 🚗🚦

A Python-based computer vision project that detects **cars only** in traffic scenes, identifies **blue cars**, counts the **total number of cars**, and also counts the **number of people** at a traffic signal using **YOLOv8** and **OpenCV**.

---

## 📌 Project Features

- Detects **cars only** (ignores bus, truck, bike, etc.)
- Detects **people** at the traffic signal
- Identifies **blue cars**
- Draws:
  - **Red rectangle** → Blue cars
  - **Blue rectangle** → Other cars
  - **Green rectangle** → People
- Displays:
  - Total Cars
  - Blue Cars
  - Other Cars
  - People Count
- GUI interface using **Tkinter**
- Supports:
  - Image upload
  - Video upload
  - Webcam/live camera detection

---

## 🛠️ Technologies Used

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- NumPy
- Pillow (PIL)
- Tkinter

---

## 📂 Project Structure

``` id="r5s7tw"
car_colour_detection_project/
│── app.py
│── detector.py
│── color_classifier.py
│── requirements.txt
│── README.md
│── .gitignore

⚙️ Installation
1. Clone the repository:
git clone https://github.com/RohitPatil4511/car-color-detection_in_traffic.git
cd car-color-detection_in_traffic

2. Install dependencies:
pip install -r requirements.txt

3. Run the project:
python app.py

🚀 How It Works
1.YOLOv8 detects objects in each frame
2.Only car objects are processed for color detection
3.The car body region is analyzed using HSV-based blue  color detection
4.If the car is blue:
  Red bounding box is drawn
5.If the car is not blue:
   Blue bounding box is drawn
6.If a person is detected:
  Green bounding box is drawn
7.Live counters are displayed in the GUI

🎯 Detection Rules:
Red box → Blue car
Blue box → Other car
Green box → Person

📊 Output Counters
The system shows:
Total Cars
Blue Cars
Other Cars
People Count

📸 Input Options
Upload an image
Upload a video
Start webcam/live camera

📦 Requirements
Install required packages:
pip install ultralytics opencv-python numpy pillow
Or use:
pip install -r requirements.txt

📷 Example Use Cases:
Traffic signal monitoring
Smart city traffic analysis
Vehicle colour-based filtering
Crowd presence detection near traffic lights
Academic computer vision mini-project

⚠️ Notes
>Best results are obtained in daylight traffic scenes
>White/silver cars may sometimes reflect sky color; improved color filtering is used to reduce false blue detection
>YOLO model file (yolov8n.pt) will be downloaded automatically by Ultralytics on first run if internet is available

👨‍💻 Author
Rohit Patil
GitHub: RohitPatil4511



