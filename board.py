import numpy as np


class Board(object):
    """棋盘类"""

    num_players = 2

    state = None

    def start(self):
        """开始"""
        pass

    def display(self):
        """显示"""
        pass

    def winner(self):
        """结束"""
        pass

    def current_player(self):
        """获取当前玩家"""
        return self.state.player_turn

    def legal_actions(self):
        """获取合法动作"""
        pass

    def is_legal(self, action):
        """动作是否合法"""
        pass

    def parse(self):
        """用户输入动作"""
        pass


class WUZI(Board):

    class State(object):

        def __init__(self, size):
            self.qipan = np.zeros((size, size), dtype='int8')  # 0:empty 1:human 2:com
            self.player_turn = True     # True: human    False: com

    size = 15

    def __init__(self):
        self.state = self.State(self.size)

    def start(self):
        """开始"""
        while True:
            try:
                player_turn = int(input("please input 0:You First, 1:Computer First:\n"))
            except Exception as e:
                print(e)
                continue
            if player_turn in (0, 1):
                break
        self.state.player_turn = player_turn == 0

    def display(self):
        """显示"""
        print('You : O')
        print('COM : X')
        show = '    '
        for i in range(self.size):
            show += '%2d ' % (i + 1)
        print(show)
        for i in range(self.size):
            show = '%2d   ' % (i + 1)
            for j in range(self.size):
                if self.state.qipan[i][j] == 0:
                    show += '+  '
                elif self.state.qipan[i][j] == 1:
                    show += 'O  '
                else:
                    show += 'X  '
            print(show)
            print('')
        pass

    def parse(self):
        """用户输入动作"""
        while True:
            try:
                action = eval(input("please input action a,b:\n"))
            except Exception as e:
                print(e)
                continue
            if len(action) == 2:
                x = action[0] - 1
                y = action[1] - 1
                if x < self.size and y < self.size:
                    if self.is_legal((x, y)):
                        self.state.qipan[x][y] = 1
                        self.state.player_turn = False
                    else:
                        print('%s is not empty' % str(action))
                else:
                    print('a or b need below %d' % self.size)

    def is_legal(self, action):
        """动作是否合法"""
        if self.state.qipan[action[0]][action[1]] == 0:
            return True
        else:
            return False

    def winner(self):
        q = self.state.qipan
        for i in range(self.size):
            for j in range(self.size):
                if q[i][j] != 0:
                    if i < self.size - 4:
                        if q[i][j] == q[i + 1][j] == q[i + 2][j] == q[i + 3][j] == q[i + 4][j]:
                            return q[i][j]
                    if j < self.size - 4:
                        if q[i][j] == q[i][j + 1] == q[i][j + 2] == q[i][j + 3] == q[i][j + 4]:
                            return q[i][j]
                    if i < self.size - 4 and j < self.size - 4:
                        if q[i][j] == q[i + 1][j + 1] == q[i + 2][j + 2] == q[i + 3][j + 3] == q[i + 4][j + 4]:
                            return q[i][j]
        return 0

    def legal_actions(self, state=None):
        s = self.state if state is None else state
        return np.transpose(np.where(s.qipan == 0))


wz = WUZI()
# wz.parse()
wz.display()
