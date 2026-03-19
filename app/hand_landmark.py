import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandLandmarkDetector:
    def __init__(self, model_path):
        self.timestamp = 0
        # load and setup model
        base_options = python.BaseOptions(model_asset_path=str(model_path))
        options = vision.HandLandmarkerOptions(base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self._callback
            )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

        self.result = None
    
    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data=rgb_frame)

        self.timestamp += 1
        self.landmarker.detect_async(mp_image, self.timestamp)
    
    def _callback(self, result, output_image, timestamp_ms):
        self.result = result