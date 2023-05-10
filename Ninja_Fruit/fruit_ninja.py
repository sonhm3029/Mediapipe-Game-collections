import cv2
from HandTracking.Hand_tracking_module import handDetector
import numpy as np
import mouse

cap = cv2.VideoCapture(0)
cam_w, cam_h = 640, 480
cap.set(3, cam_w)
cap.set(4, cam_h)


detector = handDetector(detectionCon=0.65, maxHands=1)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    PosList = detector.findPosition(img)
    if len(PosList):
        ind_x, ind_y = PosList[8][1], PosList[8][2]
        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)
        
        # Mouse
        conv_x = int(np.interp(ind_x, (0, cam_w), (0, 1536)))
        conv_y = int(np.interp(ind_y, (0, cam_h), (0, 864)))
        mouse.move(conv_x, conv_y)
    
    cv2.imshow("Camera Feed", img)
    cv2.waitKey(1)