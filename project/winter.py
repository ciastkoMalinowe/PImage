import numpy as np
import cv2

def run(frame):
	return cv2.applyColorMap(frame, cv2.COLORMAP_WINTER)
