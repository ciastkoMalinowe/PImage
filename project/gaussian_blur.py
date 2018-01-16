import numpy as np
import cv2

def run(frame):

    kernel = np.ones((3,3),np.float32)/9
    return cv2.filter2D(frame,-1,kernel)
