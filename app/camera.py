import cv2
from pathlib import Path
import numpy as np

import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = Path(__file__).resolve().parent / 'models' / 'hand_landmarker.task'

class VideoCamera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
        self.timestamp = 0

        # load and setup model
        base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
        options = vision.HandLandmarkerOptions(base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.landmark_callback
            )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

        self.result = ""
    
    def get_frame(self):
        success, frame = self.cap.read()

        if not success:
            return None
        
        frame = cv2.flip(frame, 1)  # flip the frame horizontally

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data=rgb_frame)

        self.timestamp += 1
        self.landmarker.detect_async(mp_image, self.timestamp)
        
        if self.result:
            cv2.putText(frame, self.result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # else:
        #     cv2.putText(frame, "No gesture detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

    def landmark_callback(self, result, output_image, timestamp_ms):
        if result:
            try:
                landmarks = result.hand_landmarks[0]
            except IndexError:
                self.result = ""
                return

            def finger_extended(tip, pip, wrist):
                tip_to_wrist = np.linalg.norm(np.array([tip.x - wrist.x, tip.y - wrist.y, tip.z - wrist.z]))
                pip_to_wrist = np.linalg.norm(np.array([pip.x - wrist.x, pip.y - wrist.y, pip.z - wrist.z]))

                return tip_to_wrist > pip_to_wrist
            
            index = finger_extended(landmarks[8], landmarks[6], landmarks[0])
            middle = finger_extended(landmarks[12], landmarks[10], landmarks[0])
            ring = finger_extended(landmarks[16], landmarks[14], landmarks[0])
            pinky = finger_extended(landmarks[20], landmarks[18], landmarks[0])

            if not index and not middle and not ring and not pinky:
                self.result = "Rock"
            elif index and middle and not ring and not pinky:
                self.result = "Scissors"
            elif index and middle and ring and pinky:
                self.result = "Paper"
            else:
                self.result = "Unknown"

        else:
            self.result = ""