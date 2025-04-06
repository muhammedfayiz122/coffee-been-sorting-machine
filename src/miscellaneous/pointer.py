import cv2
import numpy as np

def get_stats(image, x, y):
    pixel = image[y, x]
    mean_val = np.mean(pixel)
    median_val = np.median(pixel)
    min_val = np.min(pixel)
    max_val = np.max(pixel)
    
    hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]
    
    return {
        'Mean': mean_val,
        'Median': median_val,
        'Min': min_val,
        'Max': max_val,
        'HSV': hsv_pixel
    }

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        stats = get_stats(param, x, y)
        text = f"X: {x}, Y: {y}, Mean: {stats['Mean']:.2f}, Median: {stats['Median']:.2f}, Min: {stats['Min']}, Max: {stats['Max']}, HSV: {stats['HSV']}"
        temp_img = param.copy()
        cv2.putText(temp_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('Image', temp_img)

if __name__ == "__main__":
    image = cv2.imread('../processed_images/newly_annotated/1.jpg')  # Change to your image path
    cv2.imshow('Image', image)
    cv2.setMouseCallback('Image', mouse_callback, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 