import copy

WIN = 1
LOSE = -1
TIE = 0
CONTINUE = -999

X = 1
O = 0


class MinMaxAgent:

    def __init__(self, my_token='x'):
        self.my_token = my_token
        self.height = None
        self.width = None
    

    def decide(self, game_instance):
        self.height = game_instance.height
        self.width = game_instance.width

        
        state = game_instance.board


        actions = self.possible_drops(game_instance.board)
        generated_states = [copy.deepcopy(game_instance.board)for possiblity in actions]


        x = 0

        for index, state in enumerate(generated_states):
            self.drop_token(state, actions[index], x)

        
        results = []
        for state in generated_states:
            result = self.min_max_tree(state,x, 2)
            results.append(result)

        print(results)

        decision = results.index(max(results))
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
            #self.wins = None  # tie
            return TIE   # Tie

        for four in self.iter_fours(board_state):

            if self.my_token == 'o':
                if four == ['o', 'o', 'o', 'o']:
                    #elf.wins = 'o'
                    return WIN
                elif four == ['x', 'x', 'x', 'x']:
                    #self.wins = 'x'
                    return LOSE
                
            
            elif self.my_token == 'x':
                    if four == ['o', 'o', 'o', 'o']:
                        #elf.wins = 'o'
                        return LOSE
                    elif four == ['x', 'x', 'x', 'x']:
                        #self.wins = 'x'
                        return WIN

        return CONTINUE


    def possible_drops(self, board_state):
        return [n_column for n_column in range(self.width) if board_state[0][n_column] == '_']
    
    
    def drop_token(self, board_state, n_column, x):

        n_row = 0
        while n_row + 1 < self.height and board_state[n_row+1][n_column] == '_':
            n_row += 1

        if x == X:
            board_state[n_row][n_column] = 'x'
        
        if x == O:
            board_state[n_row][n_column] = 'o'

    

    def min_max_tree(self, board_state, x, depth = 2):


        finish = self._check_game_over(board_state)


        if depth == 0:
            return TIE  # maximum depth was achieved

        if finish == CONTINUE:
            actions = self.possible_drops(board_state)
            generated_states = [copy.deepcopy(board_state)for possiblity in actions]

            for index, state in enumerate(generated_states):
                self.drop_token(state, actions[index], x)

            

            # for b in generated_states:
            #     for row in b:
            #         print(row)


            results = []
            for index, board in enumerate(generated_states):
                result = self.min_max_tree(board, x, depth - 1)
                results.append(result)
                
            #results = [self.min_max_tree(board_copy, x, depth-1) for ]
            if x == O: # best option for player
        
                return max(results)
            
            if x == X: # worst option for opponent
                
                return min(results)




        return finish # finish 

        



        pass



