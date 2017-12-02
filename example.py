import numpy as np
import cv2

scale = 4

def paste_ellipse(destination, source, h, w):
    ellipse = np.zeros((h,w,3))
    cv2.ellipse(ellipse, (h / 2, w / 2), (h / 4 + h / 8, w / 2), 0, 0, 360, (0, 255, 0) ,-1)
    for i in range(h):
        for j in range(w):
            if(ellipse[i, j, 1] != 0):
                destination[i, j] = source[i, j]


#TODO: change fixed border width to sth not fixed
def blur_border(image, h, w) :
    blurred = cv2.blur(image, (7,7))
    ellipse = np.zeros((h, w, 3))
    cv2.ellipse(ellipse, (h / 2, w / 2), (h /4 + h/8, w / 2), 0, 0, 360, (0, 255, 0),
             20,1)
    for i in range(h):
        for j in range(w):
            if (ellipse[i, j, 1] != 0):
                if image.shape[0] > i and image.shape[1] > j:
                    image[i, j] = blurred[i, j]


#TODO: change fixed resize 10 to sth not fixed
#swaps 2 ellipses from rectangles with faces
def swap_2_faces(faces, frame):
    x,y,w,h = faces[0]
    x1,y1,w1,h1 = faces[1]
    x, y, w, h, x1, y1, w1, h1 = \
        x*scale, y*scale, w*scale, h*scale, x1*scale, y1*scale, w1*scale, h1*scale
    face = frame[y:y+h, x:x+w]
    face1 = frame[y1:y1+h1, x1:x1+w1]
    face = cv2.resize(face, (w1, h1))
    face1 = cv2.resize(face1, (w, h))
    new_x, new_y = max(0, x1-10), max(0, y1-10)
    paste_ellipse(frame[y1:y1+h1, x1:x1+w1], face, h1, w1)
    blur_border(frame[new_y:new_y+h1+20, new_x:new_x+w1+20], h1+20, w1+20)
    paste_ellipse(frame[y:y + h, x:x + w],  face1, h, w)
    new_x, new_y = max(0, x - 10), max(0, y - 10)
    blur_border(frame[new_y:new_y + h+20, new_x:new_x + w+20], h+20, w+20)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video = cv2.VideoCapture(0)
while(True):

    ret, frame = video.read()
    small = cv2.resize(frame, (640/scale,480/scale))
    small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        small,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    if len(faces) > 1:
        swap_2_faces(faces, frame)

    else:
        for (x, y, w, h) in faces:
            x, y, w, h = \
                x * scale, y * scale, w * scale, h * scale
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.ellipse(frame, (x+w/2, y+h/2),(w/4 + w/8, h/2),0,0,360,(0, 255, 0),1)

    cv2.imshow('faces', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()