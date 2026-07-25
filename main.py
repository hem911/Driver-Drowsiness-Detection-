import cv2
import time
import pygame
import pyttsx3
import threading

import os
import sys
# -------------------- INIT --------------------
pygame.mixer.init()

# Sound files (FIXED PATHS)

def resource_path(relative_path):
    """Get absolute path for development and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


WARNING_SOUND = resource_path("sounds/warning.wav")
DROWSY_SOUND = resource_path("sounds/medium.wav")
CRITICAL_SOUND = resource_path("sounds/alert-sound.mp3")

FACE_XML = resource_path("haarcascades/haarcascade_frontalface_default.xml")
EYE_XML = resource_path("haarcascades/haarcascade_eye.xml")

face_cascade = cv2.CascadeClassifier(FACE_XML)
eye_cascade = cv2.CascadeClassifier(EYE_XML)
# Voice engine
engine = pyttsx3.init()
voice_on = False

def speak(msg):
    engine.say(msg)
    engine.runAndWait()

# Haar cascades


# -------------------- VARIABLES --------------------
EYE_MISSING_FRAMES = 25
BLINK_THRESHOLD = 5

eye_missing_counter = 0
blink_count = 0
blink_frame_counter = 0
last_blink_count = 0 
start_time = None
current_sound = None

# 📊 Graph variables
time_data = []
blink_data = []
start_graph_time = time.time()
start_total_time = time.time()

cap = cv2.VideoCapture(0)
prev_time = time.time()
cv2.namedWindow("Smart Driver Monitoring System", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Smart Driver Monitoring System", 1920, 1080)
print("🚗 Smart Driver Monitoring System Started")

# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eyes_detected = False

    # -------------------- FACE + EYE --------------------
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h//2, x:x + w]

        eyes = eye_cascade.detectMultiScale(
            roi_gray, 1.1, 5, minSize=(20, 20)
        )

        if len(eyes) > 0:
            eyes_detected = True

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0,255,0), 2)

    # -------------------- DROWSINESS LOGIC --------------------
    if len(faces) > 0 and not eyes_detected:
        eye_missing_counter += 1

        if start_time is None:
            start_time = time.time()

        duration = time.time() - start_time
        blink_frame_counter += 1

    else:
        if 0 < blink_frame_counter < BLINK_THRESHOLD:
            blink_count += 1

        blink_frame_counter = 0
        eye_missing_counter = 0
        start_time = None
        duration = 0

        pygame.mixer.music.stop()
        current_sound = None
        voice_on = False

    # -------------------- STATUS --------------------
    status = "ALERT"
    color = (0, 255, 0)

    if eye_missing_counter > 15:
        status = "WARNING"
        color = (0, 255, 255)

    if eye_missing_counter > 30:
        status = "DROWSY"
        color = (0, 165, 255)

    if eye_missing_counter > 50:
        status = "CRITICAL!"
        color = (0, 0, 255)

        with open("log.txt", "a") as f:
            f.write(f"Drowsiness detected at {time.ctime()}\n")

    # -------------------- SOUND --------------------
    if status == "WARNING" and current_sound != "warning":
        pygame.mixer.music.load(WARNING_SOUND)
        pygame.mixer.music.play()
        current_sound = "warning"

    elif status == "DROWSY" and current_sound != "medium":
        pygame.mixer.music.load(DROWSY_SOUND)
        pygame.mixer.music.play()
        current_sound = "medium"

    elif status == "CRITICAL!" and current_sound != "critical":
        pygame.mixer.music.load(CRITICAL_SOUND)
        pygame.mixer.music.play(-1)
        current_sound = "critical"

        if not voice_on:
            voice_on = True
            threading.Thread(
                target=speak,
                args=("Wake up! You are drowsy",),
                daemon=True
            ).start()

    # -------------------- GRAPH DATA --------------------
    if time.time() - start_graph_time >= 2:
        elapsed_time = round(time.time() - start_total_time, 2)

        # 🔥 Calculate blink rate (difference)
        blink_rate = blink_count - last_blink_count

        time_data.append(elapsed_time)
        blink_data.append(blink_rate)

        last_blink_count = blink_count
        start_graph_time = time.time()

    # -------------------- DISPLAY --------------------
    cv2.putText(frame, f"Status: {status}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.putText(frame, f"Eye Closed: {round(duration,2)} sec", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Blinks: {blink_count}", (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    if len(faces) == 0:
        cv2.putText(frame, "FACE NOT DETECTED", (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("Smart Driver Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
import matplotlib.pyplot as plt
plt.ioff()          # Disable interactive mode
plt.close('all')    # Close any accidental figures

plt.figure(figsize=(8,5))
plt.plot(time_data, blink_data, marker='o')
plt.xlabel("Time (seconds)")
plt.ylabel("Blink Count")
plt.title("Blink vs Time Graph")
plt.grid(True)
plt.show()

# -------------------- SHOW GRAPH --------------------

