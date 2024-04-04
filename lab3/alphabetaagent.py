import copy
import logging
import time

WIN = 1
LOSE = -1
TIE = 0
CONTINUE = -999
INIT_DEPTH = 6

PLUS_INF = 999
MIN_INF = -999



class AlfaBetaAgent:

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

        alfa = PLUS_INF
        beta = MIN_INF

        for state in generated_states:
            
            if state == None:
                results.append(None)
                continue

            result = self.min_max_tree(state, 0, alfa, beta, INIT_DEPTH)
            results.append(result)


        #self.logger.info(f"res: {results}")

        max_value = max(item for item in results if item is not None)

        decision = results.index(max_value)


        # 0 is the state value which isnt showing any win/lose condition
        # so agent should check if there is a possibilty to make the move at the center

        if max_value == 0:
            decision = self.cover_center(results, decision)

        end_time = time.time()  # End time counter
        elapsed_time = end_time - start_time
        self.logger.info(f"Alfa beta: {elapsed_time} seconds")
            
        return decision



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


    def _check_game_over(self, board_state):
        if not self.possible_drops(board_state):
            return TIE   # Tie

        for four in self.iter_fours(board_state):
            if self.my_token == 'o':
                if four == ['o', 'o', 'o', 'o']:
                    return WIN
                elif four == ['x', 'x', 'x', 'x']:
                    return LOSE
                
            
            elif self.my_token == 'x':
                    if four == ['o', 'o', 'o', 'o']:
                        return LOSE
                    elif four == ['x', 'x', 'x', 'x']:
                        return WIN

        return CONTINUE


    def possible_drops(self, board_state):
        return [n_column if board_state[0][n_column] == '_' else None for n_column in range(self.width)]
    
    
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

    
    def min_max_tree(self, board_state, x, alfa, beta, depth = 4):

        finish = self._check_game_over(board_state) # checking the state of the game


        if depth == 0:
            return TIE  # maximum depth was achieved

        if finish == CONTINUE:
            actions = self.possible_drops(board_state)


            #self.logger.info(f"possible: {actions}")
            generated_states = [copy.deepcopy(board_state) for possiblity in actions]

            for index, state in enumerate(generated_states):
                self.drop_token(state, actions[index], x)
    
            if x == 0:

                results = []
                v = PLUS_INF
                cut_off = False

                for index, board in enumerate(generated_states):

                    if cut_off:
                        results.append(None)
                        continue

                    if actions[index] == None:
                        results.append(None)
                        continue
                    
                    result = self.min_max_tree(board, 1, alfa, beta, depth - 1)

                    v = min(v, result)
                    beta = min(beta, v)

                    if v <= alfa:
                        cut_off = True
                        #self.logger.info("Cut off")

                    results.append(result)
                
                return min(item for item in results if item is not None)
            
            if x == 1:

                results = []
                v = MIN_INF
                cut_off = False
            
                for index, board in enumerate(generated_states):

                    if cut_off:
                        results.append(None)
                        continue

                    if actions[index] == None:
                        results.append(None)
                        continue

                    result = self.min_max_tree(board, 0, alfa, beta, depth - 1)

                    v = max(v, result)
                    alfa = max(alfa, v)

                    if v >= beta:
                        #self.logger.info("Cut off")
                        cut_off = True

                    results.append(result)
                
                return max(item for item in results if item is not None)


        return finish # finish 



    def cover_center(self, results, first_decision):
        midpoint = len(results) // 2

        # if the midpoint can be achieved, agent should choose it
        if results[midpoint] == 0:
            return midpoint
        
        if results[midpoint-1] == 0:
            return midpoint - 1
        
        if results[midpoint+1] == 0:
            return midpoint + 1
        
        return first_decision

        
    def init_logger(self):
        self.logger = logging.getLogger('spam_application')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)

    


