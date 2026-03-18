import numpy as np

class GestureClassifier:
    def classify_gesture(self, result):
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
                return "Rock"
            elif index and middle and not ring and not pinky:
                return "Scissors"
            elif index and middle and ring and pinky:
                return "Paper"
            else:
                return "Unknown"

        else:
            return ""