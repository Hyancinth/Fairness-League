from flask import Flask, render_template
from pathlib import Path
# from app.blueprints.video.video import video_bp
from app.blueprints.game_api.game_api import game_api
from app.camera import VideoCamera
from app.controller.controller import GameController
from app import singletons

def create_app(config_object):
    app = Flask(__name__, instance_relative_config=True)
    
    MODEL_PATH = Path(__file__).resolve().parent/'models' / 'hand_landmarker.task'
    
    app.config.from_object(config_object)

    singletons.controller = GameController(MODEL_PATH)
    singletons.camera = VideoCamera()

    # app.register_blueprint(video_bp, url_prefix='/video')
    app.register_blueprint(game_api, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app