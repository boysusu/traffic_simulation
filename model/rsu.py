'''
@File   :   rsu.py
@Author :   boysusu
@Desc   :   RSU类
'''

from util.const import *


class RSU:
    def __init__(self, config):
        self.set_default_config()
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.id = None  # RSU唯一id
        self.x = 0  # RSU的x坐标
        self.y = 0  # RSU的y坐标
        self.r = 200  # 通信覆盖半径
        self.cpu = 20 * GHz  # 边缘服务器计算能力
        self.use_num_of_channels = 0  # 已使用的信道数量
        self.max_num_of_channels = 10  # 信道数量
