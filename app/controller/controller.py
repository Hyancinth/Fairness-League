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

        if landmarks and landmarks.hand_landmarks:
            hand = landmarks.hand_landmarks[0]
            h, w, _ = frame.shape
            
            # Draw bounding box around detected hand
            x_coords = [lm.x for lm in hand]
            y_coords = [lm.y for lm in hand]
            x_min = max(0, int(min(x_coords) * w) - 20)
            y_min = max(0, int(min(y_coords) * h) - 20)
            x_max = min(w, int(max(x_coords) * w) + 20)
            y_max = min(h, int(max(y_coords) * h) + 20)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 212, 0), 2)
            
            gesture = self.classifier.classify_gesture(landmarks)
            if gesture:
                self.latest_gesture = gesture.lower()
        else:
            self.latest_gesture = None
    
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
