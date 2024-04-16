import copy
import logging
import time

WIN = 1
LOSE = -1
TIE = 0


CONTINUE = -999


PLUS_INF = 999
MIN_INF = -999

class MinMaxHeur:
      def __init__(self, my_token='x'):
            self.my_token = my_token
            self.height = None
            self.width = None
            self.opponent = 'x' if self.my_token == 'o' else 'o'
            self.init_logger()

      def decide(self, game_instance):
            start_time = time.time() 
            self.height = game_instance.height
            self.width = game_instance.width

            state = game_instance.board

            actions = self.possible_drops(game_instance.board)
            #self.logger.info(f"decider: {actions}")

            generated_states = [copy.deepcopy(game_instance.board) for possiblity in actions]

            x = 1

            for index, state in enumerate(generated_states):
                  if actions[index] == None:
                        generated_states[index] = None
                        continue

                  self.drop_token(state, actions[index], x)

            results = []

            for state in generated_states:
                  
                  if state == None:
                        results.append(None)
                        continue

                  result = self.min_max_tree(state, 0, 3)
                  results.append(result)


            #self.logger.info(f"res: {results}")

            max_value = max(item for item in results if item is not None)

            decision = results.index(max_value)

            end_time = time.time()  # End time counter
            elapsed_time = end_time - start_time
            self.logger.info(f"MinMaxHeur: {elapsed_time} seconds")
                  
            return decision
      
      def evaluate_state(self, board_state):
            if not self.possible_drops(board_state):
                  return TIE   # Tie

            for four in self.iter_fours(board_state):
                  if four.count(self.my_token) == 4:
                        return WIN
                  if four.count(self.opponent) == 4:
                        return LOSE
            
            return CONTINUE
      
      def heuristic_evaluation(self, board_state):
            score = 0
            coefficient = 1
            for four in self.iter_fours(board_state):
                  if four.count(self.my_token) == 3 and four.count("_") == 1:
                        score += 0.08

                  elif four.count(self.opponent) == 3 and four.count("_") == 1:
                        score -= 0.08

                  elif four.count(self.my_token) == 2 and four.count("_") == 2:
                        score += 0.01

                  elif four.count(self.opponent) == 2 and four.count("_") == 2:
                        score -= 0.01


            center = self.center_column(board_state, self.width, self.height)
            
            center_ally_score = center.count(self.my_token) * 0.2

            #print(f"got {(center_ally_score + score) / coefficient}")
            return (center_ally_score + score) #/ coefficient
      

      def center_column(self, state, width, height):
            return [state[n_row][width//2] for n_row in range(height)]
      

      def min_max_tree(self, board_state, x, depth = 4):

            finish = self.evaluate_state(board_state) # checking the state of the game

            if finish == WIN:
                  return WIN
            
            elif finish == LOSE:
                  return LOSE
            
            elif finish == TIE:
                  return TIE

            if depth == 0:
                  return self.heuristic_evaluation(board_state)


            if finish == CONTINUE:
                  if finish == CONTINUE:
                    actions = self.possible_drops(board_state)
                        
                    #self.logger.info(f"possible: {actions}")
                    generated_states = [copy.deepcopy(board_state) for possiblity in actions]

                    for index, state in enumerate(generated_states):
                        self.drop_token(state, actions[index], x)
            
                    if x == 0: #0

                        results = []
                        for index, board in enumerate(generated_states):

                            if actions[index] == None:
                                results.append(None)
                                continue

                            result = self.min_max_tree(board, 1, depth - 1)
                            results.append(result)
                        
                        return min(item for item in results if item is not None)
                    
                    if x == 1:

                        results = []
                        for index, board in enumerate(generated_states):

                            if actions[index] == None:
                                results.append(None)
                                continue

                            result = self.min_max_tree(board, 0, depth - 1)
                            results.append(result)
                        
                        return max(item for item in results if item is not None)


            return finish # finish 




      def iter_fours(self, board_state):
            # horizontal
            for n_row in range(self.height):
                  for start_column in range(self.width-3):
                        yield board_state[n_row][start_column:start_column+4]

            # vertical
            for n_column in range(self.width):
                  for start_row in range(self.height-3):
                        yield [board_state[n_row][n_column] for n_row in range(start_row, start_row+4)]

            # diagonal
            for n_row in range(self.height-3):
                  for n_column in range(self.width-3):
                        yield [board_state[n_row+i][n_column+i] for i in range(4)]  # decreasing
                        yield [board_state[n_row+i][self.width-1-n_column-i] for i in range(4)]  # increasing

      def drop_token(self, board_state, n_column, x):

            if n_column == None:
                  return
            
            n_row = 0
            while n_row + 1 < self.height and board_state[n_row+1][n_column] == '_':
                  n_row += 1


            if x == 1:
                  board_state[n_row][n_column] = self.my_token
            
            if x == 0:
                  board_state[n_row][n_column] = self.opponent

      def possible_drops(self, board_state):
            return [n_column if board_state[0][n_column] == '_' else None for n_column in range(self.width)]

      def init_logger(self):
            self.logger = logging.getLogger('spam_application')
            self.logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler('spam.log')
            fh.setLevel(logging.DEBUG)
            self.logger.addHandler(fh)