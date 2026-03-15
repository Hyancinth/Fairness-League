from flask import Blueprint, Response
from app.camera import VideoCamera

video_bp = Blueprint('video', __name__)

camera = VideoCamera()

def gen_frames(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# route to stream video feed
@video_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')