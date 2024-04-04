from connect4 import Connect4
import random
import logging

import copy
import time
import os

class AlfaBetaAgent:
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
            score, _ = self.alfabeta(generated_state, depth = 4, alfa=float('-inf'), beta = float('inf'),maximizing_player=False)
            possibilites.append((score, column))
        
        
        end = time.time()
        self.logger.info(f"Alfabeta time : {end-start} seconds")
        return self.choose(possibilites)


    def alfabeta(self, game, depth, alfa, beta, maximizing_player):
        if depth == 0 or game.game_over:
            return self.evaluate(game), None

        if maximizing_player:
            max_eval = -99999999
            best_move = None
            for column in game.possible_drops():
                generated_state = copy.deepcopy(game)
                generated_state.drop_token(column)
                eval, _ = self.alfabeta(generated_state, depth - 1, alfa, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = column
                alfa = max(alfa, eval)
                if alfa >= beta:
                    break
            return max_eval, best_move
        else:
            min_eval = 99999999
            best_move = None
            for column in game.possible_drops():
                generated_state = copy.deepcopy(game)
                generated_state.drop_token(column)
                eval, _ = self.alfabeta(generated_state, depth - 1, alfa, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = column
                beta = min(beta, eval)
                if alfa >= beta:
                    break
            return min_eval, best_move

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
