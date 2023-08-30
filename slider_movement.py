import cv2
import numpy as np

def empty(a):
    pass

class HandDetection:
    def __init__(self):
        pass

    def create_trackbars(self):
        cv2.namedWindow('Trackbars')
        cv2.resizeWindow('Trackbars', 500, 300)
        cv2.createTrackbar('HueMin', 'Trackbars', 0, 179, empty)
        cv2.createTrackbar('HueMax', 'Trackbars', 179, 179, empty)
        cv2.createTrackbar('SatMin', 'Trackbars', 0, 255, empty)
        cv2.createTrackbar('SatMax', 'Trackbars', 206, 255, empty)
        cv2.createTrackbar('ValMin', 'Trackbars', 0, 255, empty)
        cv2.createTrackbar('ValMax', 'Trackbars', 113, 255, empty)

    def create_mask(self, img):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hue_min = cv2.getTrackbarPos('HueMin', 'Trackbars')
        hue_max = cv2.getTrackbarPos('HueMax', 'Trackbars')
        sat_min = cv2.getTrackbarPos('SatMin', 'Trackbars')
        sat_max = cv2.getTrackbarPos('SatMax', 'Trackbars')
        val_min = cv2.getTrackbarPos('ValMin', 'Trackbars')
        val_max = cv2.getTrackbarPos('ValMax', 'Trackbars')
        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])
        mask = cv2.inRange(imgHSV, lower, upper)
        return mask

    def threshold(self, mask):
        _, thresh_img = cv2.threshold(mask, 127, 255, cv2.THRESH_OTSU)
        return thresh_img

    def clean_image(self, mask):
        img_eroded = cv2.erode(mask, (3, 3), iterations=1)
        img_dilated = cv2.dilate(img_eroded, (3, 3), iterations=1)
        return img_dilated

    def find_contours(self, thresh_img):
        contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def max_contour(self, contours):
        if len(contours) == 0:
            return []
        max_cntr = max(contours, key=lambda x: cv2.contourArea(x))
        epsilon = 0.005 * cv2.arcLength(max_cntr, True)
        max_cntr = cv2.approxPolyDP(max_cntr, epsilon, True)
        return max_cntr

    def centroid(self, contour):
        if len(contour) == 0:
            return (-1, -1)
        M = cv2.moments(contour)
        try:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
        except ZeroDivisionError:
            return (-1, -1)
        return (x, y)

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