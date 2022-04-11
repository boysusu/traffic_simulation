class RSU:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.init_properties()

    def init_properties(self):
        self.cpu = 3 * 10 ** 7  # cpu计算能力
        self.r = 200  # 通信覆盖半径

