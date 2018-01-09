import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Queue
import numpy as np
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

    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        
        if not queue.empty():
            print(queue.get())
        
        cv2.imshow('TEST',FUNC[iter].run(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
def read_input():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    queue = Queue()
    filter_process = Process(target =run_filters, args=(queue,))
    filter_process.start()
    while True:
        input_quit = GPIO.input(18)
        input_forward = GPIO.input(23)
        input_back = GPIO.input(24)
        
        if input_quit== False:
            print("q pressed")
            queue.put('quit')
            time.sleep(0.5)

        if input_back==False:
            print('a pressed')
            queue.put(-1)
            time.sleep(0.5)
            
        elif input_forward==False:
            queue.put([1])
            print('s pressed')
            time.sleep(0.5)
            
            
    
read_input()
    
    
    