from app.game.rps_game import RPSGame, FixedStrategy, RandomStrategy, CopycatStrategy

def test_game_initialization():
    game = RPSGame()
    assert game.history == []
    assert game.player_move is None
    assert game.robot_move is None
    assert game.result is None
    assert game.winner is None
    assert game.player_score == 0
    assert game.robot_score == 0
    assert game.rounds_played == 0
    assert game.max_rounds == 21
    assert game.warmup_rounds == 4
    assert game.warmup_strategy is not None
    assert game.strategy is not None
    assert game.game_over == False

def test_rock_beats_scissors():
    game = RPSGame()
    round_result = game.get_round_result("rock", "scissors")
    assert round_result == "player"

def test_paper_beats_rock():
    game = RPSGame()
    round_result = game.get_round_result("paper", "rock")
    assert round_result == "player"

def test_scissors_beats_paper():
    game = RPSGame()
    round_result = game.get_round_result("scissors", "paper")
    assert round_result == "player"

def test_tie():
    game = RPSGame()
    round_result = game.get_round_result("rock", "rock")
    assert round_result == "tie"

def test_invalid_move():
    game = RPSGame()
    move = "invalid_move"
    result = game.play_round(move)
    assert "error" in result

def test_tie_does_not_increment_rounds_played():
    game = RPSGame(strategy=FixedStrategy("rock"))
    game.rounds_played = game.warmup_rounds
    game.play_round("rock")
    
    assert game.rounds_played == game.warmup_rounds

def test_tie_does_not_end_game():
    game = RPSGame(strategy=FixedStrategy("rock"))
    game.rounds_played = game.warmup_rounds
    for _ in range(game.max_rounds - game.warmup_rounds - 1):
        game.play_round("paper")
    
    game.play_round("rock")
    assert game.game_over == False
    assert game.rounds_played == game.max_rounds - 1


def test_game_over_after_max_rounds():
    game = RPSGame(strategy=FixedStrategy("rock"))
    game.rounds_played = game.warmup_rounds
    for _ in range(game.max_rounds - game.warmup_rounds):
        game.play_round("paper")
    
    assert game.game_over == True
    assert game.rounds_played == game.max_rounds

def test_winner_determination():
    game = RPSGame()
    assert game.determine_winner(player_score=5, robot_score=3) == "player"
    assert game.determine_winner(player_score=2, robot_score=4) == "robot"

def test_robot_emotion():
    game = RPSGame()
    assert game.get_robot_emotion(score_diff=3) == "ecstatic"
    assert game.get_robot_emotion(score_diff=1) == "happy"
    assert game.get_robot_emotion(score_diff=0) == "neutral"
    assert game.get_robot_emotion(score_diff=-1) == "sad"
    assert game.get_robot_emotion(score_diff=-3) == "devastated"
