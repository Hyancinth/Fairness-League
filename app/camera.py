import cv2
from pathlib import Path
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = Path(__file__).resolve().parent / 'models' / 'gesture_recognizer.task'
GESTURE_MAP = {
    "Closed_Fist": "Rock",
    "Open_Palm": "Paper",
    "Victory": "Scissors"
}

class VideoCamera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
        self.start_time = time.time()

        # load model
        base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
        options = vision.GestureRecognizerOptions(base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.recognize_callback
            )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

        self.latest_gesture = None
    
    def get_frame(self):
        success, frame = self.cap.read()

        if not success:
            return None
        
        frame = cv2.flip(frame, 1)  # flip the frame horizontally

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_mps = int((time.time() - self.start_time) * 1000)
        self.recognizer.recognize_async(mp_image, timestamp_mps)
        
        if self.latest_gesture:
            cv2.putText(frame, self.latest_gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No gesture detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

    def recognize_callback(self, result, output_image, timestamp_ms):
        if result:
            gesture = result.gestures[0][0]
            self.latest_gesture = f"{GESTURE_MAP.get(gesture.category_name, gesture.category_name)} ({gesture.score:.2f})"
        else:
            self.latest_gesture = ""