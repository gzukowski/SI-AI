from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from alfabetaagent import AlfaBetaAgent
from alphabetaagent import AlphaBetaAgent
from agent import Agent
import time

connect4 = Connect4(width=7, height=6)
agent1 = Agent('o')
agent2 = MinMaxAgent('x')
while not connect4.game_over:
    connect4.draw()
    time.sleep(1)
    try:
        if connect4.who_moves == agent1.my_token:
            n_column = agent1.decide(connect4)
        else:
            n_column = agent2.decide(connect4)
        connect4.drop_token(n_column)
    except (ValueError, GameplayException):
        print('invalid move')

connect4.draw()
