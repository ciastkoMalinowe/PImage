from Tkinter import *
from PIL import Image
from PIL import ImageTk
import threading
import cv2
import RPi.GPIO as GPIO
from subprocess import call

import canny_edge
import gaussian_blur
import face_swap
import cat_face
import negative
import blue_object
import spring
import summer
import winter
import autumn
import rainbow
import laplace
import sharpen_edges
import excessed_edges


FUNC = [canny_edge, gaussian_blur, face_swap, cat_face, negative, blue_object,
		spring, summer, winter, autumn, rainbow, laplace, sharpen_edges, excessed_edges]

DESCRIPTION = ['  EDGE DETECTION  ',
               '  GAUSSIAN_BLUR   ',
               '    SWAP FACES    ',
               '     CAT FACE     ',
               '     NEGATIVE     ',
               '    BLUE OBJECT   ',
               ' SPRING COLORMAP  ',
               ' SUMMER COLORMAP  ',
               ' WINTER COLORMAP  ',
               ' AUTUMN COLORMAP  ',
               ' RAINBOW COLORMAP ',
               '  LAPLACE FILTER  ',
               '  SHARPEN FILTER  ',
               'EXCESS EDGE FILTER']
ITER = 0
iter = 0


def display():
    global video, iter
    
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        frame = FUNC[ITER].run(frame)
        
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        
        video.configure(image=frame)
        video.image = frame

        
def display_descriptions():
    global leftLabel, centerLabel, rightLabel
    
    n = len(FUNC)
    leftLabel.configure(text = DESCRIPTION[(iter - 1 + n) % n])
    centerLabel.configure(text = DESCRIPTION[iter])
    rightLabel.configure(text = DESCRIPTION[(iter + 1) % n])
    
def key(x):
    x = x.char
    if(x == 'a'):
        left()
    if(x == 's'):
        enter()
    if(x == 'd'):
        right()
    if(x == 'q'):
        terminate()
    if(x == 'e'):
	shutdown()
        
def terminate():
    global window
    window.quit()

def shutdown():
    call("sudo shutdown -h now", shell=True)


def left():
    global iter
    iter = (iter + len(FUNC) - 1) % len(FUNC)
    display_descriptions()

def gpio_left(x):
    left()

def right():
    global iter
    iter = (iter + len(FUNC) + 1) % len(FUNC)
    display_descriptions()
    
def gpio_right(x):
    right()
    
def enter():
    global ITER
    ITER = iter

def gpio_enter(x):
    enter()

def play():
    t = threading.Thread(target=display, args=())
    t.daemon = True
    t.start()

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(18, GPIO.RISING, callback=gpio_right, bouncetime=200)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.RISING, callback=gpio_enter, bouncetime=200)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(24, GPIO.RISING, callback=gpio_left, bouncetime=200)
    

window = Tk()
window.bind('<Key>', key)

buttons = Frame(window)
buttons.pack(pady=20)
b1 = Button(buttons, text='<-', command=left)
b1.pack(side='left')
b2 = Button(buttons, text='ENTER', command=enter)
b2.pack(side='left')
b3 = Button(buttons, text='->', command=right)
b3.pack(side='left')

descriptions = Frame(window)
descriptions.pack(pady=20)
leftLabel = Label(descriptions, font=('Helvetica', 12))
leftLabel.pack(side='left')
centerLabel = Label(descriptions, font=('Helvetica', 20), bg='grey')
centerLabel.pack(side='left')
rightLabel = Label(descriptions, font=('Helvetica', 12))
rightLabel.pack(side='left')

video = Label(window)
video.pack(padx=10, pady=10)

initGPIO()
play()
display_descriptions()
window.mainloop()
