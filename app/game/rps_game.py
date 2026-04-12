import random
import time

MOVES = ["rock", "paper", "scissors"]

BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

class RandomStrategy():
    def select_move(self, history):
        return random.choice(MOVES)

class FixedStrategy():
    def __init__(self, move=None):
        self.fixed_move = move if move in MOVES else random.choice(MOVES)
    
    def select_move(self, history):
        return self.fixed_move

class CopycatStrategy():
    def select_move(self, history):
        if not history:
            return random.choice(MOVES)
        
        last_player_move = history[-1]["player"]
        return last_player_move


class RPSGame():
    def __init__(self, strategy = None):
        self.reset(strategy)
    
    def reset(self, strategy=None):
        self.history = []

        self.player_move = None
        self.robot_move = None
        self.result = None
        self.winner = None

        self.player_score = 0
        self.robot_score = 0

        self.rounds_played = 0
        self.max_rounds = 21
        self.warmup_rounds = 4

        self.warmup_strategy = RandomStrategy()
        self.strategy = strategy if self.strategy is not None else random.choice([RandomStrategy(), FixedStrategy(), CopycatStrategy()])

        self.game_over = False
    
    def pick_strategy(self):
        if self.rounds_played < self.warmup_rounds:
            return self.warmup_strategy
        
        return self.strategy
    
    def play_round(self, gesture):
        if self.game_over:
            return {"error": "Game is over"}
        if gesture not in MOVES:
            return {"error": "Invalid move"}
        
        robot_move = self.pick_strategy().select_move(self.history)
        self.result = self.get_round_result(gesture, robot_move)

        if self.result == "player":
            self.player_score += 1
        elif self.result == "robot":
            self.robot_score += 1

        if self.result != "tie":
            self.rounds_played += 1
        
        round_data = {
            "round": self.rounds_played,
            "player": self.player_move,
            "robot": self.robot_move,
            "result": self.result,
            "player_score": self.player_score,
            "robot_score": self.robot_score,
        }

        self.history.append(round_data)

        if self.result != "tie" and self.rounds_played >= self.max_rounds:
            self.game_over = True
            self.winner = self.determine_winner()

        return round_data
 
    def get_round_result(self, gesture, robot_move):
        self.player_move = gesture if gesture in MOVES else None
        self.robot_move = robot_move if robot_move in MOVES else None
        
        if self.player_move == self.robot_move:
            return "tie"
        elif BEATS[self.player_move] == self.robot_move:
            return "player"
        else:
            return "robot"
    
    def determine_winner(self, player_score=None, robot_score=None):
        if player_score is None:
            player_score = self.player_score
        if robot_score is None:
            robot_score = self.robot_score

        if player_score > robot_score:
            return "player"
        elif robot_score > player_score:
            return "robot"
        else:
            return "tie"
        
    def get_robot_emotion(self, score_diff=None):
        if score_diff is None:
            score_diff = self.robot_score - self.player_score

        if score_diff >= 3:
            return "ecstatic"
        elif score_diff > 0 and score_diff < 3:
            return "happy"
        elif score_diff == 0:
            return "neutral"
        elif score_diff < 0 and score_diff > -3:
            return "sad"
        elif score_diff <= -3:
            return "devastated"
    
    def get_game_state(self):
        return {
            "round_number": self.rounds_played,
            "total_rounds": self.max_rounds,
            "player_score": self.player_score,
            "robot_score": self.robot_score,
            "game_over": self.game_over,
            "winner": self.winner,
            "emotion": self.get_robot_emotion(),
            "history": self.history,
        }
