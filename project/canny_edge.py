import cv2

def prepare():
    pass

def run(frame):
    return cv2.Canny(frame,100,200)
