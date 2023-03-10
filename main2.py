'''
@File   :   main2.py
@Author :   boysusu
@Desc   :   主程序入口2，用于多次仿真
'''

from simulation.simulation import Simulation
from util.const import *


def run_change_size(i, j, k):
    for size in range(i, j + 1, k):
        sim = Simulation(config={'xlsx_name': f'result(size={size}).xlsx'})

        sim.create_roads([
            ((1000, -8.25), (0, -8.25), True),  # 人行道
            ((1000, -5.25), (0, -5.25)),  # 车行道
            ((1000, -1.75), (0, -1.75)),  # 车行道
            ((0, 1.75), (1000, 1.75)),  # 车行道
            ((0, 5.25), (1000, 5.25)),  # 车行道
            ((0, 8.25), (1000, 8.25), True),  # 人行道
        ])

        sim.create_rsus([
            {"id": x // 400, "x": x, "y": -8.25} for x in range(0, 1000, 400)
        ])

        sim.create_car_gen({
            "road_length": 1000,
            "lam": 1,
            "size": size,
            "car_length": 3.8,
            'min_cpu': 0.5 * GHz,
            'max_cpu': 2 * GHz
        })

        sim.create_task_gen({
            'data_size': 2 * Mbit,
            'X': 500,
        })

        sim.run(steps=9999999999999)

def run_change_data_size(i=0.5, j=5, k=0.1):
    for data_size in range(int(i * Mbit), int(j * Mbit) + 1, int(k * Mbit)):
        sim = Simulation(config={'xlsx_name': f'result(data_size={round(data_size / Mbit, 2)}Mbit).xlsx'})

        sim.create_roads([
            ((1000, -8.25), (0, -8.25), True),  # 人行道
            ((1000, -5.25), (0, -5.25)),  # 车行道
            ((1000, -1.75), (0, -1.75)),  # 车行道
            ((0, 1.75), (1000, 1.75)),  # 车行道
            ((0, 5.25), (1000, 5.25)),  # 车行道
            ((0, 8.25), (1000, 8.25), True),  # 人行道
        ])

        sim.create_rsus([
            {"id": x // 400, "x": x, "y": -8.25} for x in range(0, 1000, 400)
        ])

        sim.create_car_gen({
            "road_length": 1000,
            "lam": 1,
            "size": 20,
            "car_length": 3.8,
            'min_cpu': 0.5 * GHz,
            'max_cpu': 2 * GHz
        })

        sim.create_task_gen({
            'data_size': data_size,
            'X': 500,
        })

        sim.run(steps=9999999999999)


def run_change_X(i=100, j=1000, k=100):
    for X in range(i, j + 1, k):
        sim = Simulation(config={'xlsx_name': f'result(X={X}).xlsx'})

        sim.create_roads([
            ((1000, -8.25), (0, -8.25), True),  # 人行道
            ((1000, -5.25), (0, -5.25)),  # 车行道
            ((1000, -1.75), (0, -1.75)),  # 车行道
            ((0, 1.75), (1000, 1.75)),  # 车行道
            ((0, 5.25), (1000, 5.25)),  # 车行道
            ((0, 8.25), (1000, 8.25), True),  # 人行道
        ])

        sim.create_rsus([
            {"id": x // 400, "x": x, "y": -8.25} for x in range(0, 1000, 400)
        ])

        sim.create_car_gen({
            "road_length": 1000,
            "lam": 1,
            "size": 20,
            "car_length": 3.8,
            'min_cpu': 0.5 * GHz,
            'max_cpu': 2 * GHz
        })

        sim.create_task_gen({
            'data_size': 2.5 * Mbit,
            'X': X,
        })

        sim.run(steps=9999999999999)


def run_change_V2R_channel_bandwidth(i=20, j=120, k=10):
    for V2R_channel_bandwidth in range(i * MHz, j * MHz + 1, k * MHz):
        sim = Simulation(config={'V2R_channel_bandwidth': V2R_channel_bandwidth,
                                 'xlsx_name': f'result(V2R_channel_bandwidth={V2R_channel_bandwidth//MHz}MHz).xlsx'})

        sim.create_roads([
            ((1000, -8.25), (0, -8.25), True),  # 人行道
            ((1000, -5.25), (0, -5.25)),  # 车行道
            ((1000, -1.75), (0, -1.75)),  # 车行道
            ((0, 1.75), (1000, 1.75)),  # 车行道
            ((0, 5.25), (1000, 5.25)),  # 车行道
            ((0, 8.25), (1000, 8.25), True),  # 人行道
        ])

        sim.create_rsus([
            {"id": x // 400, "x": x, "y": -8.25} for x in range(0, 1000, 400)
        ])

        sim.create_car_gen({
            "road_length": 1000,
            "lam": 1,
            "size": 20,
            "car_length": 3.8,
            'min_cpu': 0.5 * GHz,
            'max_cpu': 2 * GHz
        })

        sim.create_task_gen({
            'X': 100,
            'data_size': 5 * Mbit
        })

        sim.run(steps=9999999999999)

if __name__ == '__main__':
    run_change_size()
    run_change_data_size()
    run_change_X()
    run_change_V2R_channel_bandwidth()
