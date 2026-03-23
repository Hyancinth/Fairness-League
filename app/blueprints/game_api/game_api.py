from flask import  Blueprint, jsonify
import app.singletons as singletons

game_api = Blueprint('game_api', __name__)

@game_api.route('/frame')
def frame():
    """
    Endpoint to get the latest frame and detected gesture
    """
    frame = singletons.camera.read_frame()
    if frame is not None:
        singletons.controller.process_frame(frame)

    frame_base64, gesture = singletons.controller.get_frame_data() # returns base64 string of the frame and the detected gesture
    return jsonify({"frame": frame_base64, "gesture": gesture})

@game_api.route('/play', methods=['POST'])
def play():
    """
    Endpoint to play a game round
    """
    result = singletons.controller.play_round()
    
    if "error" in result:
        return jsonify(result)

    game_state = singletons.controller.game.get_game_state()

    return jsonify({
        "round": result["round"],
        "player_move": result["player"],
        "robot_move": result["robot"],
        "result": result["result"],
        "player_score": result["player_score"],
        "robot_score": result["robot_score"],
        "game_over": game_state["game_over"],
        "winner": game_state["winner"],
        "emotion": game_state["emotion"],
    })

@game_api.route('/reset', methods=['POST'])
def reset():
    """
    Endpoint to reset the game
    """
    singletons.controller.game.reset()
    return jsonify({"status": "ok"})