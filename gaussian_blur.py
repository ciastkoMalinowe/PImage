import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(frame,-1,kernel)
    
    cv2.imshow('BLUR',dst)
    cv2.imshow('TEST',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()