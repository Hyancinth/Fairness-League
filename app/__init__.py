from flask import Flask, render_template
from app.blueprints.video.video import video_bp

def create_app(config_object):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object(config_object)

    app.register_blueprint(video_bp, url_prefix='/video')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app