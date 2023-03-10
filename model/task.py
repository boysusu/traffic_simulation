'''
@File   :   task.py
@Author :   boysusu
@Desc   :   计算任务类
'''

import random
from util.const import *


class Task:
    def __str__(self):
        return f'({self.data_size/Mbit}Mbit, {self.X}circles/bit, {self.complete_need_time}帧)'

    def __init__(self, config):
        self.set_default_config()
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.data_size = random.randrange(0.5 * Mbit, 2 * Mbit, 0.1 * Mbit)  # 数据量大小(bit)
        self.max_tolerated_delay = 0.5  # 最大容忍时延(s)
        self.X = random.randrange(100, 1000, 100)  # 计算复杂度(每bit数据大小所需的CPU运行周期 cycles/bit)
        self.complete_need_time = None  # 计算完成需要的总时延(s)
        self.complete_need_frame = None  # 计算完成需要的总帧数
