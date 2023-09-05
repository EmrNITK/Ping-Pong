import cv2
import numpy as np
def empty(a):
        pass
class HandDetection():
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
    
    def create_mask(self,img):
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
    
    def threshold(self,mask):
        _,thresh_img = cv2.threshold(mask,127,255,cv2.THRESH_OTSU)
        return thresh_img
    
    def find_contours(self,thresh_img):
        contours,_ = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return contours
        
    def max_contour(self,contours):
        if len(contours) == 0:
            return []
        max_cntr = max(contours,key=lambda x: cv2.contourArea(x))
        epsilon = 0.005*cv2.arcLength(max_cntr,True)  
        max_cntr = cv2.approxPolyDP(max_cntr,epsilon,True)
        return max_cntr
    def clean_image(self,mask):
        img_eroded = cv2.erode(mask,(3,3), iterations=1)  
        img_dilated = cv2.dilate(img_eroded,(3,3),iterations = 1)
        return img_dilated
    def centroid(self,contour):
        if len(contour) == 0:
            return (-1,-1)
        M=cv2.moments(contour)
        try:
            x = int(M['m10']/M['m00']) 
            y = int(M['m01']/M['m00'])
        except ZeroDivisionError:
            return (-1,-1) 
        return (x,y)

######################  DRIVER CODE   #########################
# vid = cv2.VideoCapture(0);
# HandDetection = HandDetection()
# HandDetection.create_trackbars()
# while(1):
#     _,frame = vid.read()
#     frame = cv2.flip(frame,1)
#     fullScreenFrame=frame
#     frame = frame[:290, 290:] 
#     frame = cv2.GaussianBlur(frame,(3,3),0)

#     mask = HandDetection.create_mask(frame)
#     threshImg = HandDetection.threshold(mask)
#     mask_cleaned = HandDetection.clean_image(threshImg)
#     contours = HandDetection.find_contours(mask_cleaned)
#     frame = cv2.drawContours(frame,contours,-1,(255,0,0),2) 
#     max_cntr = HandDetection.max_contour(contours) 
#     (centroid_x,centroid_y) = HandDetection.centroid(max_cntr) 
#     print(centroid_x,centroid_y)
#     cv2.imshow('video',frame)
#     cv2.imshow("mask",mask)
#     key = cv2.waitKey(10)
    
#     if key == ord('q'):
#         break
# vid.release()

# cv2.destroyAllWindows()