'''
@File   :   main.py
@Author :   boysusu
@Desc   :   主程序入口
'''

from simulation.simulation import Simulation
from visualization.window import Window
from util.const import *


def run():
    sim = Simulation()
    sim.create_roads([
        ((1000, -8.25), (0, -8.25), True),  # 人行道
        ((1000, -5.25), (0, -5.25)),  # 车行道
        ((1000, -1.75), (0, -1.75)),  # 车行道
        ((0, 1.75), (1000, 1.75)),  # 车行道
        ((0, 5.25), (1000, 5.25)),  # 车行道
        ((0, 8.25), (1000, 8.25), True),   # 人行道
    ])

    sim.create_rsus([
        {"id": x//400, "x": x, "y": -8.25} for x in range(0, 1000, 400)
    ])

    sim.create_car_gen({
        "road_length": 1000,
        "lam": 1,
        "size": 10,
        "car_length": 3.8,
        'min_cpu': 0.5 * GHz,
        'max_cpu': 2 * GHz
    })

    sim.create_task_gen({
        'min_data_size': 0.5 * Mbit,  # 最小数据量
        'max_data_size': 5 * Mbit,  # 最大数据量
        'min_X': 100,  # 最小计算复杂度
        'max_X': 1000,  # 最大计算复杂度
    })

    win = Window(sim)
    win.run()


if __name__ == '__main__':
    run()