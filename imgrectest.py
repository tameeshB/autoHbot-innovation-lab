from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
yellowLower = (29, 86, 6)
yellowUpper = (64, 255, 255)
try:
	camera = cv2.VideoCapture(0)
except:
    print('nocam')
while True:
        ret, img = camera.read()
        
        # cv2.line(img,(300,0),(300,500),(255,0,0),5)
        img = imutils.resize(img, width=600)
        cv2.line(img,(300,0),(300,500),(255,255,0),1)
        cv2.line(img,(0,170),(600,170),(255,255,0),1)
        #make dynamic
        cv2.imshow("input", img)
        key = cv2.waitKey(10)
        if key == 27:
            break

# (grabbed, frame) = camera.read()
# cv2.imshow("Frame", frame)
# time.sleep(10)
# frame = imutils.resize(frame, width=600)
# # blurred = cv2.GaussianBlur(frame, (11, 11), 0) #blur to remove noise and retain structure
# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert to the HSV color space

# # localization of the green ball 
# mask = cv2.inRange(hsv, greenLower, yellowUpper)
# mask = cv2.erode(mask, None, iterations=2) # dilations and erosions to remove any small blobs left in the mask
# mask = cv2.dilate(mask, None, iterations=2)
# # find contours in the mask and initialize the current
# # (x, y) center of the ball
# cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#     cv2.CHAIN_APPROX_SIMPLE)[-2]
# center = None
# cv2.imshow("Frame", frame)
# time.sleep(10)
# # only proceed if at least one contour was found
# if len(cnts) > 0:
#     c = max(cnts, key=cv2.contourArea)
#     ((x, y), radius) = cv2.minEnclosingCircle(c)
#     M = cv2.moments(c)
#     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

#     if radius > 5: #threshold sensitivity
#         cv2.circle(frame, (int(x), int(y)), int(radius),
#             (0, 255, 255), 2)
#         cv2.circle(frame, center, 5, (0, 0, 255), -1)
    