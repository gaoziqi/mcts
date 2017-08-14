import time
import random


class TreeNode(object):

    isRoot = False
    current_action = None
    children = []

    def __init__(self, arg):
        if 'isRoot' in arg:
            self.isRoot = arg['isRoot']
        if 'current_action':
            self.current_action = arg['current_action']


class MCTS(object):

    def __init__(self, board, time=5, max_actions=1000):
        self.board = board
        self.time = time
        self.max_actions = max_actions

    def get_action(self):
        begin = time.time()
        actions = 0
        while time.time() - begin < self.time and actions < self.max_actions:
            self.simulation(self.board)
            actions += 1

    def simulation(board):
        pass
