import numpy as np
import cv2

lower_blue = None
upper_blue = None


def prepare():

    global lower_blue, upper_blue
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])


def run(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
    return cv2.bitwise_and(frame, frame, mask=mask)

prepare()

