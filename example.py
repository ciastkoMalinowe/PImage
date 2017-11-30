import numpy as np
import cv2

scale = 4

#swaps 2 rectangles with faces
def swap_2_faces(faces, frame):
    x,y,w,h = faces[0]
    x1,y1,w1,h1 = faces[1]
    x, y, w, h, x1, y1, w1, h1 = \
        x*scale, y*scale, w*scale, h*scale, x1*scale, y1*scale, w1*scale, h1*scale
    face = frame[y:y+h, x:x+w]
    face1 = frame[y1:y1+h1, x1:x1+w1]
    face = cv2.resize(face, (w1, h1))
    face1 = cv2.resize(face1, (w, h))
    frame[y1:y1+h1, x1:x1+w1], frame[y:y+h, x:x+w] = face, face1

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