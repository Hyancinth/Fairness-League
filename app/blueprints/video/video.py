import cv2
from pathlib import Path
from flask import Blueprint, Response
from app.camera import VideoCamera
from app.hand_landmark import HandLandmarkDetector
from app.gesture_classifier import GestureClassifier

video_bp = Blueprint('video', __name__)

MODEL_PATH = Path(__file__).resolve().parents[2] / 'models' / 'hand_landmarker.task'

camera = VideoCamera()
detector = HandLandmarkDetector(MODEL_PATH)
classifier = GestureClassifier()

def get_frame():
    frame = camera.read_frame()
    if frame is None:
        return None

    detector.detect(frame)
    result = detector.result
    gesture = classifier.classify_gesture(result)
    if gesture:
        cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()


def gen_frames(camera):
    while True:
        frame = get_frame()
        if frame:
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# route to stream video feed
@video_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')