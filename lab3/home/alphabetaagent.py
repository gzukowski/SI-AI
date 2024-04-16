from connect4 import Connect4
import random
from minmaxagent import pick_best_move
import copy

INIT_DEPTH = 4

INF_MIN = -999999
INF_PLUS = 999999

WIN = 1
LOSE = -1

CONTINUE = 0


class AlphaBetaAgent:
    def __init__(self, my_token):
        self.my_token = my_token
        self.opponent_token = 'x' if self.my_token == 'o' else 'o'

    def decide(self, game):
        if game.who_moves == self.my_token and game.is_Board_Empty():
            return random.choice(game.possible_drops())
        possible_moves = []
        for column in game.possible_drops():
            game_copy = copy.deepcopy(game)
            game_copy.drop_token(column)
            
            alfa = INF_MIN
            beta = INF_PLUS
            score, _ = self.alphabeta(game_copy, alfa, beta, depth = 4, x = 0)
            possible_moves.append((score, column))
        return pick_best_move(possible_moves)


    def alphabeta(self, game, alfa, beta , depth, x):
        if depth == 0 or game.game_over:
            return self.evaluate_board_heuristic(game), None

        if x:
            min_ev = INF_MIN
            best_move = None
            for column in game.possible_drops():
                game_copy = copy.deepcopy(game)
                game_copy.drop_token(column)
                v, _ = self.alphabeta(game_copy, alfa, beta, depth - 1, 0)
                if v > min_ev:
                    min_ev = v
                    best_move = column
                alfa = max(alfa, v)
                if alfa >= beta:
                    break
            return min_ev, best_move
        else:
            v = INF_PLUS
            best_move = None
            for column in game.possible_drops():
                game_copy = copy.deepcopy(game)
                game_copy.drop_token(column)
                eval, _ = self.alphabeta(game_copy, alfa, beta,  depth - 1, 0)
                if eval < v:
                    v = eval
                    best_move = column
                beta = min(beta, eval)
                if alfa >= beta:
                    break
            return v, best_move


    def evaluate_board_heuristic(self, game):
        if game.wins == self.my_token:
            return WIN 
        elif game.wins == self.opponent_token:
            return LOSE 
        else:
            score = 0

            if game.center_column().count(self.my_token) > game.center_column().count(self.opponent_token):
                score += 0.1

            
            for four in game.iter_fours():
                    if four.count(self.my_token) == 3:
                            score += 0.2

                    elif four.count(self.opponent_token) == 3:
                            score -= 0.2

                    if four.count(self.my_token) == 2:
                            score += 0.05

                    elif four.count(self.opponent_token) == 2:
                            score -= 0.05
            
            return score
