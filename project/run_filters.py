import time
from multiprocessing import Process
import cv2

import face_swap
import canny_edge
import gaussian_blur
import cat_face
import negative
import color
import blue_object

FUNC = [canny_edge, gaussian_blur, face_swap, cat_face, negative, blue_object, color]

def run_filters(queue):
    iter = 0
    FUNC[iter].prepare()
    cap = cv2.VideoCapture(0)

    while True:

        if not queue.empty():
            message = queue.get()
            if message == 'quit':
                cap.release()
                cv2.destroyAllWindows()
                return

            iter += message
            FUNC[iter].prepare()

        ret, frame = cap.read()
        cv2.imshow('FILTERS',FUNC[iter].run(frame))

    cap.release()
    cv2.destroyAllWindows()