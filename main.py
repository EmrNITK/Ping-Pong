import cv2
import numpy as np
from hand_detection import HandDetection

# Initialize video capture
vid = cv2.VideoCapture(0)

# Create an instance of HandDetection
hand_detection = HandDetection()
hand_detection.create_trackbars()

# Initialize slider variables
slider_x = 100
slider_y = 400  # Adjust the starting position to move it near the bottom
slider_width = 150  # Increase the width to make it horizontal
slider_height = 20  # Decrease the height for a horizontal slider
slider_color = (0, 255, 0)

while vid.isOpened():
    _, frame = vid.read()
    frame = cv2.flip(frame, 1)
    fullScreenFrame = frame
    frame = frame[:500, :]

    mask = hand_detection.create_mask(frame)

    threshImg = hand_detection.threshold(mask)
    mask_cleaned = hand_detection.clean_image(threshImg)
    contours = hand_detection.find_contours(mask_cleaned)
    frame = cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
    max_cntr = hand_detection.max_contour(contours)
    (centroid_x, centroid_y) = hand_detection.centroid(max_cntr)

    # Update the slider's position based on the centroid_x value
    slider_x = int((centroid_x / frame.shape[1]) * (frame.shape[1] - slider_width))  # Scale centroid_x for horizontal slider
    if slider_x < 0:
        slider_x = 0
    if slider_x + slider_width > frame.shape[1]:
        slider_x = frame.shape[1] - slider_width

    cv2.rectangle(frame, (slider_x, slider_y), (slider_x + slider_width, slider_y + slider_height), slider_color, -1)

    print(centroid_x, centroid_y)
    cv2.imshow('Hand Gesture Slider', frame)

    key = cv2.waitKey(10)

    if key == ord('q'):
        break

# Release the video capture and close all OpenCV windows
vid.release()
cv2.destroyAllWindows()