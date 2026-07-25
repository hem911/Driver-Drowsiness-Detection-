# 🚗 Smart Driver Monitoring System

A real-time **Driver Drowsiness Detection System** developed using **Python** and **OpenCV** to improve road safety by monitoring the driver's eyes through a webcam. The system detects drowsiness, provides multi-level alerts using audio and voice notifications, logs drowsiness events, and visualizes blink activity with a graph.

---

## 📌 Features

- 👤 Real-time Face Detection
- 👁️ Eye Detection using Haar Cascade
- 😴 Driver Drowsiness Detection
- ⚠️ Multi-Level Alert System
  - Alert
  - Warning
  - Drowsy
  - Critical
- 🔊 Audio Alerts
- 🗣️ Voice Alert using pyttsx3
- 👀 Blink Detection & Blink Counter
- 📊 Blink vs Time Graph
- 📝 Drowsiness Event Logging
- 🎥 Real-time FPS Display
- 🖥️ Standalone Windows Executable Support

---

## 🛠️ Technologies Used

- Python
- OpenCV
- Haar Cascade Classifiers
- Pygame
- pyttsx3
- Matplotlib

---

## 📂 Project Structure

```
Driver-Drowsiness-Detection/
│
├── haarcascades/
│   ├── haarcascade_frontalface_default.xml
│   └── haarcascade_eye.xml
│
├── sounds/
│   ├── warning.wav
│   ├── medium.wav
│   └── alert-sound.mp3
│
│
├── demo/
│   └── Driver Monitoring.mp4
│
├── main.py
├── requirements.txt
├── README.md
```

---

## 🔄 Working Flow

```
Webcam
   │
   ▼
Face Detection
   │
   ▼
Eye Detection
   │
   ▼
Eye Closure Monitoring
   │
   ▼
Blink Detection
   │
   ▼
Alert Classification
   │
   ├── Warning
   ├── Drowsy
   └── Critical
   │
   ▼
Audio + Voice Alerts
   │
   ▼
Event Logging
   │
   ▼
Blink Analysis Graph
```

---

## 🎥 Demo

A demonstration video is available in the **demo/** folder.

```
demo/Driver Monitoring.mp4
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/hem911/Driver-Drowsiness-Detection-.git
```

### Navigate to Project

```bash
cd Driver-Drowsiness-Detection-
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## 📈 Output

- Detects driver's face and eyes in real time.
- Measures eye closure duration.
- Counts blinks.
- Displays current alert status.
- Plays warning and critical sounds.
- Provides voice alert during critical drowsiness.
- Records drowsiness events.
- Displays Blink vs Time graph after exiting.

---

## 🚀 Future Improvements

- MediaPipe Face Mesh
- Eye Aspect Ratio (EAR)
- Yawn Detection
- Head Pose Estimation
- Mobile Application
- Cloud Logging
- Driver Analytics Dashboard
- Deep Learning-based Detection

---

## 👨‍💻 Author

**Kadiri Hemanth Kumar**

- GitHub: https://github.com/hem911
- LinkedIn: https://www.linkedin.com/in/kadiri-hemanth-kumar-92aa71260/

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
