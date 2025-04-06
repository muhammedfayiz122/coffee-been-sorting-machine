import serial
import time
import cv2
from ultralytics import YOLO
from utils.logger import logging
import os
from preprocess import detect_and_annotate_darkest_box
coffee_beans_class = {
    0: "dark",
    1: "light",
    2: "medium"
}

def retry_arduino_connection():
    """Retries Arduino connection in case of an error."""
    print("Retrying Arduino connection...")
    try:
        arduino.close()
    except:
        pass  # Ignore errors while closing
    arduino = None
    i=0
    while not arduino:
        try:
            arduino = serial.Serial('COM5', 9600, timeout=1)
            send_to_arduino("START")
        except:
            i+=1
            print(f"Failed to reconnect to Arduino, retrying[{i}]...")
            time.sleep(0.5)
    print("Reconnected to Arduino successfully.")
    return arduino
    

def send_to_arduino(command):
    """Sends data to Arduino, appending a newline for proper termination."""
    full_command = command + "\n"
    try:
        arduino.write(full_command.encode('utf-8'))
        # Minimal delay to allow Arduino to process the command
    except Exception as e:
        print(f"Error writing to Arduino: {e}")
        logging.error(f"Error writing to Arduino: {e}")
        try:
            retry_arduino_connection()  # Retry connection if error occurs
            intialize_arduino()  # Reinitialize Arduino communication
        except Exception as e:
            print(f"Error reinitializing Arduino: {e}")


print("Process starting...")
# Initialize serial communication with a higher baud rate (if desired)
logging.info("Initializing serial communication with Arduino...")
arduino = None
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    send_to_arduino("START")
except:
    retry_arduino_connection()  # Retry connection if error occurs
time.sleep(1)  # Allow Arduino to initialize
print("arduino opened successfully")
logging.info("Serial communication with Arduino initialized successfully.")

# Load YOLO model (replace 'best11.pt' with your trained model if needed)
print("loading model...")
model = YOLO("../models/best11.pt")
print("model loaded successfully")
logging.info("YOLO model loaded successfully.")

def capture_image():
    """Captures an image and saves it."""
    print("Capturing image from phone...")
    logging.info("Capturing image from phone...")
    # Uncomment below to use an actual video feed
    cap = cv2.VideoCapture('http://192.168.1.11:8080/video', cv2.CAP_FFMPEG)
    ret, frame = cap.read()
    if ret:
        logging.info("Image captured successfully.")
        image_path = "bean_image.jpg"
        cropped_frame = frame[918:1228, 1220:1692]
        # Save the cropped image
        cv2.imwrite(image_path, cropped_frame)
        return image_path
    else:
        logging.error("Error capturing image.") # Log error
        print("Error capturing image")
        image_path = ""
        return image_path

def classify_bean(image_path):
    """Runs YOLO on the captured image and returns the detected class."""
    img = cv2.imread(image_path)
    # Convert image to grayscale to evaluate brightness
    darkest, _, _ = detect_and_annotate_darkest_box(img)
    print(f"darkest value : {darkest}")
    if darkest > 120:
        print("lowest dark value , skipping")
        return None
    results = model(img, conf=0.6)
    detected_classes = [result.boxes.cls.tolist() for result in results]
    if detected_classes and len(detected_classes[0]) > 0:
        bean_class = int(detected_classes[0][0])  # Use first detected class
        confidence_score = results[0].boxes.conf[0].item()  # Get confidence score for the first detection
        print(f"Detected Class: {coffee_beans_class[bean_class]}, Confidence Score: {confidence_score}")
    if detected_classes and len(detected_classes[0]) > 0:
        bean_class = int(detected_classes[0][0])  # Use first detected class
        # Get the YOLO result for the first detection
        result = results[0]
        # Get bounding box coordinates (x1, y1, x2, y2) for the first detection
        xyxy = result.boxes.xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = xyxy

        # Annotate the image with the bounding box and class label by copying the cropped image
        img = img.copy()
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # cv2.putText(img, str(bean_class), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Save the annotated image (it will be saved with a new filename)
        # annotated_folder = "../processed_images/newly_annotated"
        annotated_folder = "processed_images/newly_annotated"

        annotated_folder = os.path.abspath(annotated_folder)  # Resolve to absolute path
        if not os.path.exists(annotated_folder):
            os.makedirs(annotated_folder)
        # Create unique file names for annotated image and cropped box image using current timestamp
        timestamp = int(time.time() * 1000)
        annotated_image_path = os.path.join(annotated_folder, f"annotated_{timestamp}.jpg")
        
        # Save detected bounding box as a separate cropped image in a different folder
        # boxes_folder = "../processed_images/boxes"
        boxes_folder = "processed_images/boxes"
        if not os.path.exists(boxes_folder):
            os.makedirs(boxes_folder)
        cropped_image = img[y1:y2, x1:x2]
        cropped_image_path = os.path.join(boxes_folder, f"box_{timestamp}.jpg")
        cv2.imwrite(cropped_image_path, cropped_image)
        # Calculate the middle point of the rectangle
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        # Use a larger font scale and thicker line for bold text
        cv2.putText(img, str(bean_class), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
        cv2.putText(img, f"X:{mid_x} Y:{mid_y}", (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Annotate the middle point coordinates on the image
        cv2.putText(img, f"x", (mid_x + 10, mid_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.imwrite(annotated_image_path, img)
        logging.info(f"Annotated image saved successfully for class : {bean_class}")

        return bean_class
    else:
        return None  # No detection

def read_from_arduino():
    """Reads data from Arduino."""
    try:
        response = arduino.readline().decode('utf-8').strip()
        if response:
            print(f"Arduino response: {response}")
            return response
    except Exception as e:
        print(f"Error reading from Arduino: {e}")
        logging.error(f"Error reading from Arduino: {e}")
        retry_arduino_connection()  # Retry connection if error occurs
        intialize_arduino()  # Reinitialize Arduino communication
    return None

def wait_for_response(expected_response, timeout=5):
    """
    Waits for a specific response from Arduino.
    
    Parameters:
      expected_response (str): The expected response string.
      timeout (int): Timeout in seconds.
    
    Returns:
      True if the expected response is received within the timeout period, else False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = arduino.readline().decode('utf-8').strip()
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            response = ""
        if response:
            print(f"Arduino response recieved : {response}")
            if response == expected_response:
                return True
    return False

def intialize_arduino():
    """Initializes Arduino communication."""
    print("Waiting for Arduino to signal readiness...")
    start_time = time.time()
    while time.time() - start_time < 10:  # Timeout after 10 seconds
        if read_from_arduino() == "READY":
            break
        else:
            send_to_arduino("START")
            time.sleep(0.5)
    else:
        print("Timeout waiting for Arduino to signal readiness.")
        logging.error("Timeout waiting for Arduino to signal readiness.")
        return False
    return True
    

def main():

    if intialize_arduino():
        logging.info("Received READY signal from Arduino. Starting sorting process...")
        print("Arduino is ready. Starting sorting process...")

    try:
        current_bean = 1
        while True:
            try:
                sorted_count
            except NameError:
                sorted_count = 0
            # If a bean was successfully classified in the previous cycle, update the counter.
            # (Assumes bean_class was set earlier in the loop; reset it after counting.)
            bean_class_value = locals().get('bean_class', None)
            if bean_class_value is not None:
                sorted_count += 1
                logging.info(f"Total beans sorted so far: {sorted_count}")
                bean_class = None
            logging.info("-" * 60)
            # Wait for Arduino's stepper motor completion signal
            arduino_response = read_from_arduino()
            if arduino_response == "READY":
                print("-" * 60)
                print("Arduino is ready for the next step.")
                print("Stepper motor stopped, capturing image...")
                attempts = 0
                bean_class = None
                while attempts < 2 and bean_class is None:
                    image_path = capture_image()
                    if not image_path:
                        print("Error capturing image, skipping. <continue>")
                        # send_to_arduino("STEP")
                        continue
                    bean_class = classify_bean(image_path)  # YOLO classification
                    if bean_class is None:
                        print(f"Attempt {attempts + 1} failed, retrying...")
                    attempts += 1
                    send_to_arduino(str(current_bean))
                    logging.info(f"sented to arduino : {bean_class}")
                    if bean_class is None:
                        print("Failed to detect bean class after 2 attempts, skipping.")
                        send_to_arduino("STEP")
                        print("Arduino is ready for the next step.")
                        time.sleep(0.3)
                        attempts = 0
                        current_bean = 1
                        continue


                        logging.info("Failed to detect bean class after 2 attempts, skipping.")
                        current_bean = 1
                        #if no class detected , skipping whole process
                    else:
                        print(f"Detected Class: {bean_class}")
                        logging.info(f"current bean = {bean_class} && previous bean = {current_bean}")
                        current_bean = bean_class
                    # In both cases, command the Arduino to rotate the stepper
                    logging.info("Rotating stepper motor...") 

                    send_to_arduino("STEP")
                    time.sleep(1)
                    print("-" * 60)
                    print("\n" * 1)
            else:
                time.sleep(0.1)  # Short delay if no response received
    except KeyboardInterrupt:
        print("Terminating...")
        send_to_arduino("STOP")  # Send stop signal to Arduino
    except Exception as e:
        print(f"Error: {e}")
    finally:
        arduino.close()

if __name__ == "__main__":
    main()