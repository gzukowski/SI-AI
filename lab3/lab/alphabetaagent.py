from connect4 import Connect4
import random


def pick_best_move(possible_moves):
    scores = [x[0] for x in possible_moves]
    max_score = max(scores)
    best_moves = [x[1] for x in possible_moves if x[0] == max_score]
    return random.choice(best_moves)


class AlphaBetaAgent:
    def __init__(self, my_token):
        self.my_token = my_token
        self.opponent_token = 'x' if self.my_token == 'o' else 'o'

    def decide(self, game):
        if game.who_moves == self.my_token:
            return random.choice(game.possible_drops())
        possible_moves = []
        for column in game.possible_drops():
            game_copy = self._copy_game_state(game)
            game_copy.drop_token(column)
            score, _ = self._alphabeta(game_copy, depth = 5, alpha=float('-inf'), beta = float('inf'),maximizing_player=False)
            possible_moves.append((score, column))
        return pick_best_move(possible_moves)


    def _alphabeta(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.game_over:
            return self._evaluate_board_heuristic(game), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for column in game.possible_drops():
                game_copy = self._copy_game_state(game)
                game_copy.drop_token(column)
                eval, _ = self._alphabeta(game_copy, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = column
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for column in game.possible_drops():
                game_copy = self._copy_game_state(game)
                game_copy.drop_token(column)
                eval, _ = self._alphabeta(game_copy, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = column
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return min_eval, best_move

    def _evaluate_board(self, game):
        if game.wins == self.my_token:
            return 1
        elif game.wins == self.opponent_token:
            return -1
        else:
            return 0

    def _evaluate_board_heuristic(self, game):
        if game.wins == self.my_token:
            return 1  # Wysoka nagroda za wygraną
        elif game.wins == self.opponent_token:
            return -1  # Wysoka kara za przegraną
        else:
            # Inicjalizacja punktów
            score = 0

            # Nagroda za przejęcie środka planszy
            if game.center_column().count(self.my_token) > game.center_column().count(self.opponent_token):
                score += 0.1

            # Ocena dwójek i trójek gracza
            for four in game.iter_fours():
                my_tokens = four.count(self.my_token)
                opponent_tokens = four.count(self.opponent_token)
                if my_tokens == 2:
                    score += 0.05
                elif my_tokens == 3:
                    score += 0.2
                if opponent_tokens == 2:
                    score -= 0.05
                elif opponent_tokens == 3:
                    score -= 0.2

            return score

    def _copy_game_state(self, game):
        game_copy = Connect4(width=game.width, height=game.height)
        game_copy.board = [row[:] for row in game.board]
        game_copy.who_moves = game.who_moves
        game_copy.game_over = game.game_over
        game_copy.wins = game.wins
        return game_copy
