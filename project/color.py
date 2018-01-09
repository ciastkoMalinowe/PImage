import numpy as np
import cv2

EFFECT = {'spring': cv2.COLORMAP_SPRING,
          'autumn': cv2.COLORMAP_AUTUMN,
          'winter': cv2.COLORMAP_WINTER,
          'summer': cv2.COLORMAP_SUMMER,
          'rainbow': cv2.COLORMAP_RAINBOW,
          }
effect = None


def prepare(e):

    global effect
    effect = e


def run(frame):

    return cv2.applyColorMap(frame, EFFECT[effect])
