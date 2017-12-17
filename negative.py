import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    
    negative = cv2.bitwise_not(frame)
    
    cv2.imshow('negative',negative)
    cv2.imshow('TEST',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
