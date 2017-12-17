import numpy as np
import cv2

def run_canny_edge():
    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()

        edges = cv2.Canny(frame,100,200)

        cv2.imshow('EDGES',edges)
        cv2.imshow('TEST',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
