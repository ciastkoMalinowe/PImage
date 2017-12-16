import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def blue():
    while(True):
        ret, frame = cap.read()
        
        #color = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #color = cv2.cvtColor(frame, cv2.COLOR_LUV2BGR)
        #COLOR_RGB2YUV
        #COLOR_RGB2LAB - lightness
        #HLS
        col = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        color = cv2.applyColorMap(col, cv2.COLORMAP_SPRING)
        
        cv2.imshow('frame',frame)
        cv2.imshow('blue',color)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

blue()

cap.release()
cv2.destroyAllWindows()
