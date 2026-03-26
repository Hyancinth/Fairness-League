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
    def __init__(self):
        self.fixed_move = random.choice(MOVES)
    
    def select_move(self, history):
        return self.fixed_move

class CopycatStrategy():
    def select_move(self, history):
        if not history:
            return random.choice(MOVES)
        
        last_player_move = history[-1]["player"]
        return last_player_move


class RPSGame():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.history = []

        self.player_move = None
        self.robot_move = None
        self.result = None
        self.winner = None
        self.prev_result = None

        self.player_score = 0
        self.robot_score = 0

        self.rounds_played = 0
        self.max_rounds = 21
        self.warmup_rounds = 4

        self.warmup_strategy = RandomStrategy()
        self.strategy = random.choice([RandomStrategy(), FixedStrategy(), CopycatStrategy()])

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
        
        self.process_player_move(gesture)

        if self.result == "player":
            self.player_score += 1
        elif self.result == "robot":
            self.robot_score += 1

        if self.prev_result != "tie":
            self.rounds_played += 1
        
        self.prev_result = self.result
        
        round_data = {
            "round": self.rounds_played,
            "player": self.player_move,
            "robot": self.robot_move,
            "result": self.result,
            "player_score": self.player_score,
            "robot_score": self.robot_score,
        }

        self.history.append(round_data)

        if self.rounds_played >= self.max_rounds:
            self.game_over = True
            if self.player_score > self.robot_score:
                self.winner = "player"
            elif self.robot_score > self.player_score:
                self.winner = "robot"
            else:
                self.winner = "tie"

        return round_data
 
    def process_player_move(self, gesture):
        self.player_move = gesture if gesture in MOVES else None
        self.robot_move = self.pick_strategy().select_move(self.history)
        
        if self.player_move == self.robot_move:
            self.result = "tie"
        elif BEATS[self.player_move] == self.robot_move:
            self.result = "player"
        else:
            self.result = "robot"
        
    def get_robot_emotion(self):
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
