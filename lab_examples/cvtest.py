import numpy as np
import cv2

img = cv2.imread('lena', 1)
grayscale_img = cv2.imread('lena', 0)
cv2.imshow('lena', img)
cv2.imshow('grayscal lena', grayscale_img)
cv2.waitKey(0)
cv2.destroyAllWindows()