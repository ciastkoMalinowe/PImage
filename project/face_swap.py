import numpy as np
import cv2
"""
scale = 4

def paste_ellipse(destination, source, h, w):
    ellipse = np.zeros((h,w,3))
    cv2.ellipse(ellipse, (h / 2, w / 2), (h / 4 + h / 8, w / 2), 0, 0, 360, (0, 255, 0) ,-1)
    for i in range(h):
        for j in range(w):
            if(ellipse[i, j, 1] != 0):
                destination[i, j] = source[i, j]



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
"""
scale = 8

def create_ellipse_mask():
    h = 256
    w = 256
    ellipse = np.zeros((h, w, 1),dtype=np.uint8)
    cv2.ellipse(ellipse, (h / 2, w / 2), (h / 4 + h / 8, w / 2), 0, 0, 360, 1, -1)
    return ellipse[:,:,0]


def create_blur_mask():
    h = 256
    w = 256
    ellipse = np.zeros((h, w, 1), dtype=np.uint8)
    cv2.ellipse(ellipse, (h / 2, w / 2), (h / 2, w / 2 + w/8), 0, 0, 360, 1, -1)
    cv2.ellipse(ellipse, (h / 2, w / 2), (h / 4, w / 4 + w/8), 0, 0, 360, 0, -1)

    return ellipse[:, :, 0]


def paint(destination, source, mask):
    # foreground
    fg = cv2.bitwise_or(source, source, mask=mask)
    # background
    mask = cv2.bitwise_not(mask)
    bk = cv2.bitwise_or(destination, destination, mask=mask)
    # foreground+background
    destination = cv2.bitwise_or(fg, bk)
    return destination


def paint_face(destination, source, mask):
    h = destination.shape[0]
    w = destination.shape[1]
    H = mask.shape[0]
    W = mask.shape[1]
    mask = cv2.resize(mask, (0, 0), fx=((w * 1.) / W), fy=((h * 1.) / H))
    source = cv2.resize(source, (w, h))
    return paint(destination, source, mask)


def blur_edge(destination, mask):
    h = destination.shape[0]
    w = destination.shape[1]
    H = mask.shape[0]
    W = mask.shape[1]
    mask = cv2.resize(mask, (0, 0), fx=((w * 1.) / W), fy=((h * 1.) / H))
    #source = cv2.medianBlur(destination,15)
    source = cv2.blur(destination, (7,7))
    return paint(destination, source, mask)


def swap_2_faces(faces, frame, mask, blur_mask):

    x, y, w, h = faces[0]
    x1, y1, w1, h1 = faces[1]
    x, y, w, h, x1, y1, w1, h1 = \
        x * scale, y * scale, w * scale, h * scale, x1 * scale, y1 * scale, w1 * scale, h1 * scale

    face = frame[y:y + h, x:x + w]
    face1 = frame[y1:y1 + h1, x1:x1 + w1]
    blur_width = 32
    frame[y1:y1 + h1, x1:x1 + w1] = paint_face(frame[y1:y1 + h1, x1:x1 + w1],face,mask)
    frame[y:y + h, x:x + w] = paint_face(frame[y:y + h, x:x + w], face1, mask)
    one = frame[max(y1-h1/blur_width,0):min(y1 + h1 + h1/blur_width,frame.shape[0]),
              max(x1-w1/blur_width, 0): min(x1 + w1 + w1/blur_width,frame.shape[1]) ]
    one = blur_edge(one, blur_mask)
    two = frame[max(y - h/blur_width,0) : min(y + h + h/blur_width, frame.shape[0]),
              max(x - w/blur_width, 0) : min(x + w + w/blur_width, frame.shape[1] )]
    two = blur_edge(two, blur_mask)

    return frame

def run_swap():
    scale = 8
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    maskA = create_ellipse_mask()
    blur_mask = create_blur_mask()
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
            frame = swap_2_faces(faces, frame, maskA, blur_mask)

        else:
            for (x, y, w, h) in faces:
                x, y, w, h = \
                    x * scale, y * scale, w * scale, h * scale
                blur_width = 32
                cv2.ellipse(frame, (x+w/2, y+h/2),(w/4 + w/8, h/2),0,0,360,(0, 255, 0),1)
                frame[y - h / blur_width:y + h + h / blur_width, x - w / blur_width:x + w + w / blur_width] = \
                    blur_edge(frame[max(y - h/blur_width,0) : min(y + h + h/blur_width, frame.shape[0]),
                              max(x - w/blur_width, 0): min(x + w + w/blur_width, frame.shape[1])], blur_mask)

        cv2.imshow('faces', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()