import cv2
from pathlib import Path
import numpy as np


class VideoCamera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
    
    def read_frame(self):
        success, frame = self.cap.read()

        if not success:
            return None
        
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        return frame