#import necessary libraries
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import RPi.GPIO as GPIO
import time

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

#clockwise rotation function
def clkrot:
  GPIO.output(Motor1a,GPIO.HIGH)
	GPIO.output(Motor1b,GPIO.LOW)
  GPIO.output(Motor2a,GPIO.LOW)
	GPIO.output(Motor2b,GPIO.HIGH)
  time.sleep(10)
def fwd:
  def clkrot:
  GPIO.output(Motor1a,GPIO.HIGH)
	GPIO.output(Motor1b,GPIO.LOW)
  GPIO.output(Motor2a,GPIO.HIGH)
	GPIO.output(Motor2b,GPIO.LOW)
def stopbot:
  GPIO.output(Motor1a,GPIO.LOW)
	GPIO.output(Motor1b,GPIO.LOW)
  GPIO.output(Motor2a,GPIO.LOW)
	GPIO.output(Motor2b,GPIO.LOW)

#clkw rotation till detects green object
  #while no green object detected, rotate clockwise
  #if detected stop rotation
clkrot()
#find green object coordinates
stopbot()
#align

#move towards green object
  #once in direction of object, move in a straight line towards the object
  #stop when at a specific distance from the object
fwd()
#ultrasonic distance threshold
stopbot()

  
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

#goes towards yellow base
  #once in direction of base, move in a straight line towards the base
  #stop when at a specific distance from the centre of the base

#lowers arm and opens claw
  #lower the arm such that object touches the base
  #open the claw

#lifts the arm
  #lift the arm at the same height as before
GPIO.cleanup()
