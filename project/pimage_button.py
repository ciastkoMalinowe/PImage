#import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Queue
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
    print('new process')
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
        cv2.imshow('FILTERS', FUNC[iter].run(frame))

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    queue = Queue()
    filter_process = Process(target =run_filters, args=(queue,))
    filter_process.start()
    while True:
        #input_state = GPIO.input(18)
        pressed = cv2.waitKey(1)
        if pressed & 0xFF == ord('q'):
            print("q pressed")
            queue.put('quit')
            filter_process.join()
            break

        if pressed & 0xFF == ord('a'):
            print('a pressed')
            queue.put(-1)
        elif pressed & 0xFF == ord('s'):
            print('s pressed')
            queue.put(1)

