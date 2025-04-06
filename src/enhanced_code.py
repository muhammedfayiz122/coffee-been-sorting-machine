import cv2
import time
import os
from ultralytics import YOLO
import serial
import datetime
import logging

# ---------------------- CONFIGURATION ----------------------
VIDEO_STREAM_URL = "http://192.168.31.43:8080/video"
IMAGE_FOLDER = "classified_beans"
BRIGHTNESS_THRESHOLD = 120
ARDUINO_PORT = 'COM5'
ARDUINO_BAUD_RATE = 9600
MAX_RETRIES = 2
DELAY_BETWEEN_CLASSIFICATION = 0.5  # seconds

# ---------------------- INITIAL SETUP ----------------------
model = YOLO("../models/best11.pt")  # Load trained model
arduino = None
logging.basicConfig(level=logging.INFO)

# ---------------------- ARDUINO COMMUNICATION ----------------------
def initialize_arduino():
    global arduino
    try:
        arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE)
        time.sleep(2)
        logging.info("Arduino connected.")
    except serial.SerialException as e:
        logging.error(f"Failed to connect to Arduino: {e}")
        arduino = None

def retry_arduino_connection():
    global arduino
    for attempt in range(MAX_RETRIES):
        logging.info(f"Retrying Arduino connection... Attempt {attempt + 1}")
        initialize_arduino()
        if arduino:
            return
        time.sleep(1)
    logging.error("Arduino not connected after retries.")

def send_to_arduino(command: str):
    if arduino is None or not arduino.is_open:
        logging.warning("Arduino not connected. Retrying...")
        retry_arduino_connection()
    if arduino and arduino.is_open:
        try:
            arduino.write(command.encode())
            logging.info(f"Sent to Arduino: {command}")
        except serial.SerialException as e:
            logging.error(f"Failed to send to Arduino: {e}")

# ---------------------- IMAGE PROCESSING ----------------------
def capture_frame():
    cap = cv2.VideoCapture(VIDEO_STREAM_URL)
    if not cap.isOpened():
        logging.error("Failed to open camera stream.")
        return None
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def is_bright_enough(image, threshold=BRIGHTNESS_THRESHOLD):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = hsv[..., 2].mean()
    logging.info(f"Image brightness: {brightness}")
    return brightness >= threshold

def save_image(image, bean_class):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{IMAGE_FOLDER}/{bean_class}_{timestamp}.jpg"
    cv2.imwrite(filename, image)
    logging.info(f"Saved image: {filename}")

def annotate_image(image, boxes, classes):
    for box, label in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 0), 2)
    return image

# ---------------------- CLASSIFICATION ----------------------
def classify_bean(image):
    results = model(image)
    result = results[0]
    boxes = result.boxes.xyxy.cpu().numpy()
    class_indices = result.boxes.cls.cpu().numpy().astype(int)
    class_names = [model.names[i] for i in class_indices]
    confidences = result.boxes.conf.cpu().numpy()

    if len(boxes) > 0:
        bean_class = class_names[0]
        confidence = confidences[0]
        logging.info(f"Detected: {bean_class} with confidence: {confidence:.2f}")
        annotated = annotate_image(image.copy(), boxes, class_names)
        save_image(annotated, bean_class)
        return bean_class
    else:
        logging.info("No bean detected.")
        return None

# ---------------------- MAIN LOOP ----------------------
def main():
    initialize_arduino()
    while True:
        frame = capture_frame()
        if frame is None:
            continue

        if is_bright_enough(frame):
            bean_class = classify_bean(frame)
            if bean_class:
                send_to_arduino(bean_class)
            else:
                logging.info("No classification to send.")
            time.sleep(DELAY_BETWEEN_CLASSIFICATION)
        else:
            logging.info("Image too dark. Waiting...")

if __name__ == "__main__":
    main()
