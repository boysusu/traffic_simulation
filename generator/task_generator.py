'''
@File   :   task_generator.py
@Author :   boysusu
@Desc   :   计算任务创建器
'''

from model.task import Task
import random
from util.const import *

class TaskGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.min_data_size = 0.5 * Mbit
        self.max_data_size = 5 * Mbit
        self.data_size = None
        self.X = None
        self.min_X = 100
        self.max_X = 1000
        self.max_tolerated_delay = 0.5

    def generate_tasks(self, num):
        tasks = []
        for i in range(num):
            if self.data_size is not None:
                data_size = self.data_size
            else:
                data_size = random.randrange(self.min_data_size, self.max_data_size, 0.1 * Mbit)
            if self.X is not None:
                X = self.X
            else:
                X = random.randrange(self.min_X, self.max_X, 50)
            task_config = {
                'data_size': data_size,
                'X': X
            }
            tasks.append(Task(task_config))
        return tasks


