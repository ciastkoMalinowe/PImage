import numpy as np
import cv2


def prepare():
    pass

def run(frame):

    kernel = np.ones((5,5),np.float32)/25
    return cv2.filter2D(frame,-1,kernel)
