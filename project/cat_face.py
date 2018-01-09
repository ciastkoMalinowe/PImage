#from scipy import misc
import numpy as np
import cv2


def create_mask(file_path):
    image = cv2.imread(file_path, -1)
    if(image.shape[2] != 4):
        print("No alpha channel! Unable to create a mask.")
    mask = image[:,:,3]
    return mask


def detect_face(image, face_cascade, scale):
    small_image = cv2.resize(image, (0, 0), fx=(1. / scale), fy=(1. / scale))
    gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.1, 5)


def print_with_mask(destination, x, y, w, h, image, mask):
    W = image.shape[0]
    H = image.shape[1]
    small_image = cv2.resize(image, (0, 0), fx=((w*1.) / W), fy=((h*1.) / H))
    small_mask = cv2.resize(mask, (0, 0), fx=((w*1.) / W), fy=((h*1.) / H))
    W = small_image.shape[0]
    H = small_image.shape[1]
    x = int(x)
    y = int(y)
    # foreground
    fg = cv2.bitwise_or(small_image, small_image, mask=small_mask)
    # background
    small_mask = cv2.bitwise_not(small_mask)
    roi = destination[y:y + W, x:x + H]
    bk = cv2.bitwise_or(roi, roi, mask=small_mask)
    # foreground+background
    destination[y:y + W, x:x + H] = cv2.bitwise_or(fg, bk)
    return destination

scale = None
face_cascade = None
cat = None
mask = None


def prepare():

    global scale, face_cascade, cat, mask
    scale = 8.
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    cat = cv2.imread('cat.png')
    mask = create_mask('cat.png')


def run(frame):

    faces = detect_face(frame, face_cascade, scale)

    for (x, y, w, h) in faces:
        x, y, w, h = x*scale, y*scale, w*scale, h*scale
        frame = print_with_mask(frame, x, y, w, h,cat,mask)
    return frame