import numpy as np
import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
cat = cv2.imread('cat.png', -1)
mask = cv2.imread('cat.png', 0)
small_cat = cv2.add(np.zeros((cat.shape[0],cat.shape[1],3), np.uint8), cat, mask=mask)
while(True):
    ret, frame = cap.read()
    
    old_x = frame.shape[1]
    old_y = frame.shape[0]
    
    #r = 100.0 / frame.shape[1]
    #dim = (100, int(frame.shape[0] * r))
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1)
    
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for(x,y,w,h) in faces:
        #cv2.rectangle(frame, (x*10,y*10), (w*10+x*10, y*10+h*10), (255, 255, 0), 2)
        #cv2.rectangle(small_frame, (x,y), (w+x, y+h), (255, 255, 0), 2)
        small_cat = cv2.resize(cat, (0,0), fx=(w*10/cat.shape[0]), fy=(h*10/cat.shape[1]))
        small_mask = cv2.resize(mask, (0,0), fx=(w*10/cat.shape[0]), fy=(h*10/cat.shape[1]))
        frame[y*10:y*10+small_cat.shape[0], x*10:x*10+small_cat.shape[1]] = \
            cv2.add(frame[y*10:y*10+small_cat.shape[0],
                    x*10:x*10+small_cat.shape[1]],small_cat, mask = small_mask)
    #cv2.imshow('CAT', small_cat)
    cv2.imshow('FACES',frame)
    cv2.namedWindow('FACES', cv2.WINDOW_NORMAL)
    #cv2.imshow('SMALL_FACES',small_frame)
    #cv2.namedWindow('SMALL_FACES', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('FACES', 300,300)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()