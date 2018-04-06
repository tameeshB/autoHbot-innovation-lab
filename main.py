#import necessary libraries
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import RPi.GPIO as GPIO
import time

def errlog(code):
    #placeholder for error handler

#initialize motor gpios, servo gpios, camera, usonicsensors, etc
GPIO.setmode(GPIO.BOARD)

#DC Motor
Motor1a = 16    # Input Pin
Motor1b = 18    # Input Pin
Motor2a = 26    # Input Pin
Motor2b = 28    # Input Pin

GPIO.setup(Motor1a,GPIO.OUT)
GPIO.setup(Motor1b,GPIO.OUT)
GPIO.setup(Motor2a,GPIO.OUT)
GPIO.setup(Motor2b,GPIO.OUT)

#servo
GPIO.setup(22, GPIO.OUT) 
pwm=GPIO.PWM(22,100)

#https://github.com/jrosebr1/imutils/blob/master/bin/range-detector
#image processing init
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
yellowLower = (1, 0, 255)
yellowUpper = (39, 155, 255)

# if a video path was not supplied, grab the reference
# to the webcam
try:
    camera = cv2.VideoCapture(0)
except:
    errlog(1)#cam error


#clockwise rotation function
def clkrot:
    GPIO.output(Motor1a,GPIO.HIGH)
    GPIO.output(Motor1b,GPIO.LOW)
    GPIO.output(Motor2a,GPIO.LOW)
    GPIO.output(Motor2b,GPIO.HIGH)
def cclkrot:
    GPIO.output(Motor1a,GPIO.LOW)
    GPIO.output(Motor1b,GPIO.HIGH)
    GPIO.output(Motor2a,GPIO.HIGH)
    GPIO.output(Motor2b,GPIO.LOW)

 # time.sleep(1)#change later based on theta
def fwd:
    GPIO.output(Motor1a,GPIO.HIGH)
    GPIO.output(Motor1b,GPIO.LOW)
    GPIO.output(Motor2a,GPIO.HIGH)
    GPIO.output(Motor2b,GPIO.LOW)
def stopbot:
    GPIO.output(Motor1a,GPIO.LOW)
    GPIO.output(Motor1b,GPIO.LOW)
    GPIO.output(Motor2a,GPIO.LOW)
    GPIO.output(Motor2b,GPIO.LOW)

#scan for object in one frame
def findColRange(colLow, colHigh):
    width = camera.get(3)
    height = camera.get(4)
    ratio = height/width
    nw = 600
    nwb = int(nw/2)
    nh = nw * ratio
    nhb = int(nh/2)
    whCnt = 0
    while True:
        whCnt += 1
        ret, frame = camera.read()
        # cv2.line(frame,(300,0),(300,500),(255,0,0),5)
        frame = imutils.resize(frame, width=nw)
        # cv2.line(frame,(300,0),(300,500),(255,255,0),1)
        # cv2.line(frame,(0,nhb),(600,nhb),(255,255,0),1)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0) #blur to remove noise and retain structure
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2) # dilations and erosions to remove any small blobs left in the mask
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea) #max contor area
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            centerRel = (int(M["m10"] / M["m00"]) - nwb, int(M["m01"] / M["m00"]) - nhb)
            print(centerRel)
            
            if radius > 5: #threshold sensitivity for drawing circle
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            break
            return centerRel
        else:
            if whCnt > 50:
                return False
        cv2.imshow("input", frame)
        key = cv2.waitKey(10)
        if key == 27:
            break


#clkw rotation till detects green object
  #while no green object detected, rotate clockwise
  #if detected stop rotation
#steps of 5 seconds
objCoord = False
while True:
    clkrot()
    sleep(5)
    stopbot()
    objCoord = findColRange(greenLower,greenUpper)
    if objCoord == False:
        continue
    else:
        break
#find green object coordinates

#align

#aligning and centering object
if objCoord != False:
    while objCoord[0] > 5 or objCoord[0] < -5:
        if objCoord[0] < 0:
            cclkrot()
            sleep(1)
        elif objCoord[0] > 0:
            clkrot()
            sleep(1)


#move towards green object
  #once in direction of object, move in a straight line towards the object
  #stop when at a specific distance from the object
if objCoord != False and objCoord[0] < 5 and objCoord[0] > -5:
    fwd()
#ultrasonic distance threshold

    # stopbot()

  
#lower arm wrap arm around the object
  #lower the arm such that claw is around the object
  #close the claw


pwm.start(5)
 
angle1=10
duty1= float(angle1)/10 + 2.5               ## Angle To Duty cycle  Conversion
 
angle2=160
duty2= float(angle2)/10 + 2.5
 
ck=0
while ck<=5:
     pwm.ChangeDutyCycle(duty1)
     time.sleep(0.8)
     pwm.ChangeDutyCycle(duty2)
     time.sleep(0.8)
     ck=ck+1
time.sleep(1)

#lift arm
  #lift the arm at the same height as before

#clkw rotaton till detects yellow base
  #while no yellow base detected, rotate clockwise
  #if detected stop rotation
baseCoord = False
while True:
    clkrot()
    sleep(5)
    stopbot()
    baseCoord = findColRange(yellowLower,yellowUpper)
    if baseCoord == False:
        continue
    else:
        break

if baseCoord != False:
    while baseCoord[0] > 15 or baseCoord[0] < -15:
        if baseCoord[0] < 0:
            cclkrot()
            sleep(1)
        elif baseCoord[0] > 0:
            clkrot()
            sleep(1)

#goes towards yellow base
  #once in direction of base, move in a straight line towards the base
  #stop when at a specific distance from the centre of the base
if baseCoord != False and baseCoord[0] < 5 and baseCoord[0] > -5:
    fwd()
#ultrasonic distance threshold

    # stopbot()

#lowers arm and opens claw
  #lower the arm such that object touches the base
  #open the claw

#lifts the arm
  #lift the arm at the same height as before

GPIO.cleanup()
camera.release()
cv2.destroyAllWindows()