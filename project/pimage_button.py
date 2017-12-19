import RPi.GPIO as GPIO
import time
from multiprocessing import Process

from face_swap import run_swap
from canny_edge import run_canny_edge
from gaussian_blur import run_gaussian_blur
from cat_face import run_cat_face
from negative import run_negative
from color import run_color
from blue_object import run_blue_object

FILTERS = {'canny_edge': run_canny_edge,
           'blur': run_gaussian_blur,
           'face_swap': run_swap,
           'cat_face': run_cat_face,
           'negative': run_negative,
           'blue_object': run_blue_object,
           'color': run_color
           }
FUNC = [run_canny_edge, run_gaussian_blur, run_swap, run_cat_face, run_negative,
           run_blue_object, run_color]
COLORS = ['spring', 'summer', 'autumn', 'winter', 'rainbow']
iter = 0
itr_color = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
my_process = Process(target ='canny_edge')
my_process.start()
while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)
        my_process.terminate()
        func = FUNC[iter]
        if func == run_color:
            
            my_process = Process(target =func, args=(COLORS[itr_color]))
            my_process.start()
            if(itr_color + 1 < len(COLORS)):
                itr_color += 1
            else:
                itr_color = 0;
                iter = 0
        else:
            iter += 1
            my_process = Process(target =func)
            my_process.start()

