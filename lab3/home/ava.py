from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from alphabetaagent import AlphaBetaAgent
import time
connect4 = Connect4(width=7, height=6)
agent1 = MinMaxAgent('x')
agent2 = AlphaBetaAgent('o')
while not connect4.game_over:
    connect4.draw()
    try:
        if connect4.who_moves == agent1.my_token:
            start_time_agent1 = time.time()
            n_column = agent1.decide(connect4)
            end_time_agent1 = time.time()
            time_agent1 = end_time_agent1-start_time_agent1
            print("It took me ", time_agent1, " to decide on the move - agent1")
        else:
            start_time_agent2 = time.time()
            n_column = agent2.decide(connect4)
            end_time_agent2 = time.time()
            time_agent2 = end_time_agent2 - start_time_agent2
            print("It took me ", time_agent2, " to decide on the move - agent2")
        connect4.drop_token(n_column)
    except (ValueError, GameplayException):
        print('invalid move')

connect4.draw()
