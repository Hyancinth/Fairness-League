import base64
import cv2 
from app.hand_landmark import HandLandmarkDetector
from app.gesture_classifier import GestureClassifier
from app.game.rps_game import RPSGame

class GameController:
    def __init__(self, model_path):
        self.detector = HandLandmarkDetector(model_path)
        self.classifier = GestureClassifier()
        self.game = RPSGame()

        self.latest_frame = None
        self.latest_gesture = None
    
    def process_frame(self, frame):
        self.latest_frame = frame
        self.detector.detect(frame)
        landmarks = self.detector.result

        if landmarks:
            gesture = self.classifier.classify_gesture(landmarks)
            if gesture:
                self.latest_gesture = gesture.lower()
    
    def get_frame_data(self):
        if self.latest_frame is not None:
            _, buffer = cv2.imencode('.jpg', self.latest_frame) # encode frame as jpg
            return base64.b64encode(buffer).decode('utf-8'), self.latest_gesture # return base64 string of the frame and the detected gesture
        
        return None

    def play_round(self):
        if self.latest_gesture:
            result = self.game.play_round(self.latest_gesture)
            return result
        
        return {"error": "No gesture detected"}
