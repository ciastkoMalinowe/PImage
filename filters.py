import numpy as np
import cv2


vertical_edges = np.array([[0,0,-1,0,0],[0,0,-1,0,0],[0,0,4,0,0],[0,0,-1,0,0],[0,0,-1,0,0]])
horizontal_edges = np.array([[0,0,-1,0,0],[0,0,-1,0,0],[0,0,2,0,0],[0,0,0,0,0],[0,0,0,0,0]])
edges45 = np.array([[-1,0,0,0,0],[0,-2,0,0,0],[0,0,6,0,0],[0,0,0,-2,0],[0,0,0,0,-1]])
laplace = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]])
sharpen = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
excess_edges = np.array([[1,1,1],[1,-7,1],[1,1,1]])
gauss = np.array([[1, 1, 2, 1, 1], [1, 2, 4, 2, 1], [2, 4, 8, 4, 2], [1, 2, 4, 2, 1], [1, 1, 2, 1, 1]], np.float32) / 52

def apply(frame, filter):
    return cv2.filter2D(frame, -1, filter)

video = cv2.VideoCapture(0)

while(True):

    ret, frame = video.read()
    frame = apply(frame, laplace)

    cv2.imshow('faces', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()