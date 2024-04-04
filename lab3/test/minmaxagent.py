from connect4 import Connect4
import random
import copy
import logging
import time
import os



class MinMaxAgent:
    def __init__(self, my_token):
        self.my_token = my_token
        self.opponent_token = 'x' if self.my_token == 'o' else 'o'
        self.init_logger()

    def decide(self, game):
        
        start = time.time()
        if game.who_moves == self.my_token and game.is_Board_Empty():
            return random.choice(game.possible_drops())
        possibilites = []
        
        
        for column in game.possible_drops():
            generated_state = copy.deepcopy(game)
            generated_state.drop_token(column)
            score = self.min_max_tree(generated_state, depth=4, x=False)
            possibilites.append((score, column))

        end = time.time()
        
        self.logger.info(f"Minmax time : {end-start} seconds")
        return self.choose(possibilites)

    def min_max_tree(self, game, depth, x):
        if depth == 0 or game.game_over:
            return self.evaluate(game)

        if x:
            max_eval = -999999
            for column in game.possible_drops():
                generated_state = copy.deepcopy(game)
                generated_state.drop_token(column)
                eval = self.min_max_tree(generated_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = 999999
            for column in game.possible_drops():
                game_copy = copy.deepcopy(game)
                game_copy.drop_token(column)
                eval = self.min_max_tree(game_copy, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval


    def evaluate(self, game):
        if game.wins == self.my_token:
            return 1
        elif game.wins == self.opponent_token:
            return -1

        score = 0

        if game.center_column().count(self.my_token) > game.center_column().count(self.opponent_token):
            score += 0.1

        for four in game.iter_fours():
            if four.count(self.my_token) == 2:
                score += 0.05
            elif four.count(self.my_token) == 3:
                score += 0.2
                
                
            if four.count(self.opponent_token) == 2:
                score -= 0.05
            elif four.count(self.opponent_token) == 3:
                score -= 0.2

        return score

    
    def choose(self, possible_moves):
        results = []
        for move in possible_moves:
            results.append(move[0])
        
        max_score = max(results)
        
        best = []
        for move in possible_moves:
            if move[0] == max_score:
                best.append(move[1])
        
        return random.choice(best)
    
    def init_logger(self):
        if os.path.exists("spam.log"):
            with open("spam.log", "w"):
                pass 
        self.logger = logging.getLogger('spam_application')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
