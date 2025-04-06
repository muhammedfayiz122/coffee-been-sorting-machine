import cv2
import numpy as np
import os
import datetime

def detect_and_annotate_darkest_box(frame, save_folder="../processed_images/darkest_point", box_size=(30, 30)):
    """
    Detects the darkest region in an image using a sliding window approach with a larger box size.
    
    Parameters:
        frame (numpy.ndarray): The input image in BGR format.
        save_folder (str): The folder path to save the annotated image.
        box_size (tuple): The dimensions (width, height) of the window.
    
    Returns:
        annotated_frame (numpy.ndarray): The annotated image with the darkest region marked.
        save_path (str): The path where the annotated image is saved.
    """
    # Ensure the save folder exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    box_h, box_w = box_size

    min_avg_intensity = float('inf')
    darkest_top_left = (0, 0)
    
    # Slide a window over the image to compute the average intensity for each patch
    for y in range(0, h - box_h + 1, box_h // 2):  # Step half box size for better accuracy
        for x in range(0, w - box_w + 1, box_w // 2):
            patch = gray[y:y+box_h, x:x+box_w]
            avg_intensity = np.mean(patch)
            if avg_intensity < min_avg_intensity:
                min_avg_intensity = avg_intensity
                darkest_top_left = (x, y)
    
    # Draw annotation
    annotated_frame = frame.copy()
    cv2.rectangle(annotated_frame, 
                  darkest_top_left, 
                  (darkest_top_left[0] + box_size[0], darkest_top_left[1] + box_size[1]), 
                  (0, 255, 0), 2)
    cv2.putText(annotated_frame, f"{min_avg_intensity:.1f}", 
                (darkest_top_left[0], darkest_top_left[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
    # Generate a unique filename using the current timestamp
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    save_path = os.path.join(save_folder, filename)
    cv2.imwrite(save_path, annotated_frame)
    
    return min_avg_intensity, annotated_frame, save_path
