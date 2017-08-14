class State(object):
    player_turn = 0


class Board(object):
    """棋盘类"""

    num_players = 2

    def start(self):
        """开始"""
        pass

    def display(self, state):
        """显示"""
        pass

    def winner(self, state):
        """结束"""
        pass

    def current_player(self, state):
        """获取当前玩家"""
        return state.player_turn

    def legal_actions(self, state):
        """获取合法动作"""
        pass

    def is_legal(self, action, state):
        """动作是否合法"""
        pass

    def parse(self, action):
        """用户输入动作"""
        pass

    def next_state(self, action, state=None):
        """下一个状态"""
        pass


class WUZI(Board):

    size = 15

    class WUZIState(State):

        def __init__(self, _size):
            size = _size

    def __init__(self):
        state = WUZIState(self.sizecd )

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
        self.state['player_turn'] = player_turn == 1

    def display(self, state):
        """显示"""

        pass


wz = WUZI()
wz.start()
