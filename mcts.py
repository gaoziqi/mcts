import time
import random


class TreeNode(object):

    isRoot = False
    board = None
    last_action = None
    children = []
    father = None
    value = None

    def init(self, board, last_action=None, root=False, father=None):
        self.isRoot = root
        self.board = board
        self.last_action = last_action
        self.father = father
        self.children = []
        self.value = None


class MCTS(object):

    def __init__(self, time=5, max_actions=1000):
        self.node = TreeNode()
        self.time = time
        self.max_actions = max_actions

    def get_action(self, board, last_action):
        begin = time.time()
        actions = 0
        if self.node.board is None:
            self.node.init(board, root=True)
        else:
            node = None
            for i in self.node.children:
                if i.last_action == last_action:
                    node = i
            if node is None:
                self.node.board = board
        while time.time() - begin < self.time and actions < self.max_actions:
            self.simulation(self.node)
            actions += 1

    def simulation(node):
        pass
