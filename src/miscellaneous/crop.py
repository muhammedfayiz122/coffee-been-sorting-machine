import cv2
import numpy as np

# Global variables for drawing the ROI (Region of Interest)
drawing = False     # True while drawing ROI
ix, iy = -1, -1     # Initial x,y coordinates of the ROI
ex, ey = -1, -1     # Ending x,y coordinates of the ROI
roi_selected = False  # True when ROI is finalized

resize_factor = 0.5

def draw_axes(img):
    """Draw horizontal and vertical axes in the center of the image."""
    h, w = img.shape[:2]
    # Draw vertical axis (blue)
    cv2.line(img, (w // 2, 0), (w // 2, h), (255, 0, 0), 1)
    # Draw horizontal axis (blue)
    cv2.line(img, (0, h // 2), (w, h // 2), (255, 0, 0), 1)

def mouse_callback(event, x, y, flags, param):
    """Mouse callback to draw a cropping rectangle."""
    global ix, iy, ex, ey, drawing, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        roi_selected = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ex, ey = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ex, ey = x, y
        roi_selected = True

def main():
    global drawing, roi_selected, ix, iy, ex, ey
    cap = cv2.VideoCapture('http://192.168.188.49:8080/video')
    ret, frame = cap.read()
    if frame is None:
        print("Image not found.")
        return
    window_name = 'Frame'

    temp_frame = cv2.resize(frame, (int(frame.shape[1] * resize_factor), int(frame.shape[0] * resize_factor)))

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    while True:
        display_frame = temp_frame.copy()

        # Draw axes on the frame
        draw_axes(display_frame)

        # Draw the cropping rectangle if drawing or if ROI is selected
        if drawing or roi_selected:
            cv2.rectangle(display_frame, (ix, iy), (ex, ey), (0, 255, 0), 2)

        cv2.imshow(window_name, display_frame)
        key = cv2.waitKey(1) & 0xFF

        # Press 'c' to crop the current frame based on the drawn ROI
        if key == ord('c') and roi_selected:
            # Determine top-left and bottom-right points
            x1, y1 = int(ix / resize_factor), int(iy / resize_factor)
            x2, y2 = int(ex / resize_factor), int(ey / resize_factor)
            cropped = frame[y1:y2, x1:x2]
            cv2.imshow('Cropped', cropped)
            print(f"Cropped Coordinates: Top-Left ({x1}, {y1}), Bottom-Right ({x2}, {y2})")

        # Press 'r' to reset the ROI selection
        elif key == ord('r'):
            roi_selected = False

        # Press ESC key to exit
        elif key == 27:
            break

    # cap.release()
    #cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()