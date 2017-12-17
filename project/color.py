import numpy as np
import cv2

EFFECT = {'spring': cv2.COLORMAP_SPRING,
          'autumn': cv2.COLORMAP_AUTUMN,
          'winter': cv2.COLORMAP_WINTER,
          'summer': cv2.COLORMAP_SUMMER,
          'rainbow': cv2.COLORMAP_RAINBOW,
          }


def run_color(effect):
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()

        # color = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # color = cv2.cvtColor(frame, cv2.COLOR_LUV2BGR)
        # COLOR_RGB2YUV
        # COLOR_RGB2LAB - lightness
        # HLS
        color = cv2.applyColorMap(frame, EFFECT[effect])

        cv2.imshow('frame', frame)
        cv2.imshow('blue', color)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
