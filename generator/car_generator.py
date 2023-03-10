'''
@File   :   car_generator.py
@Author :   boysusu
@Desc   :   汽车创建器
'''

import random

from model.car import Car
from util.const import *
from numpy.random import poisson


class CarGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        """Set default configuration"""
        self.road_length = 1000
        self.lam = 1
        self.size = 40
        self.car_length = 3.8
        self.min_cpu = 0.2 * GHz
        self.max_cpu = 2 * GHz

    def generate_cars(self):
        car_id = 0
        for k in range(len(self.sim.roads)):
            if self.sim.roads[k].is_bicycle:  # 人行道跳过
                continue
            poisson_list = poisson(lam=self.lam, size=self.size)  # 泊松分布序列
            l = self.road_length / self.size - self.car_length / 2  # 每单位段长度
            for i in range(self.size):
                if poisson_list[i] == 0:
                    continue
                d = l / poisson_list[i]  # 每单位段内的均匀分布间距
                for j in range(poisson_list[i]):
                    x = i * (self.road_length / self.size) + self.car_length / 2 + j * d
                    car = Car({
                        "id": car_id,  # 车辆编号
                        "x": round(x, 2),  # 车辆x坐标
                        "y": self.sim.roads[k].start[1],  # 车辆y坐标
                        "current_road_index": k,  # 车辆所处的车道编号
                        "angle_cos": self.sim.roads[k].angle_cos,  # 车辆行驶方向与x轴的余弦值
                        "cpu": random.randrange(self.min_cpu, self.max_cpu, 0.1 * GHz),  # 车载cpu计算能力
                    })
                    car_id += 1
                    self.sim.cars.append(car)
                    if self.sim.roads[k].angle_cos == 1:
                        self.sim.roads[k].cars.add(car)
                    else:
                        self.sim.roads[k].cars.append(car)
        return car_id

            # for car in road.cars.ergodic:
            #     print(car.data.x,end=',')
            # print()

    def update(self):
        for road in self.sim.roads:
            if road.is_bicycle:
                continue
            head_car = road.cars.head.data
            if 0 <= head_car.x <= self.road_length:
                continue
            # 车辆移出范围时重置位置
            if head_car.x > self.road_length:
                head_car.x = 0
            elif head_car.x < 0:
                head_car.x = self.road_length

            # 车辆或移出范围时移除task记录
            if head_car.id in self.sim.has_task_car_id_set | self.sim.cooperating_car_id_set:
                if head_car.need_collaborative_car_id is not None:  # 作为协同节点的汽车
                    self.sim.has_task_car_id_set.remove(head_car.need_collaborative_car_id)
                    self.sim.cooperating_car_id_set.remove(head_car.id)
                    self.sim.cars[head_car.need_collaborative_car_id].task = None
                    self.sim.cars[head_car.need_collaborative_car_id].collaborative_car_id = None
                    head_car.need_collaborative_car_id = None
                elif head_car.collaborative_car_id is not None:  # 由其他汽车协同计算的汽车
                    self.sim.has_task_car_id_set.remove(head_car.id)
                    self.sim.cooperating_car_id_set.remove(head_car.collaborative_car_id)
                    head_car.task = None
                    self.sim.cars[head_car.collaborative_car_id].need_collaborative_car_id = None
                    head_car.collaborative_car_id = None
                elif head_car.collaborative_rsu_id is not None:  # 由RSU协同计算的汽车
                    self.sim.rsus[head_car.collaborative_rsu_id].use_num_of_channels -= 1
                    head_car.collaborative_rsu_id = None
                    self.sim.has_task_car_id_set.remove(head_car.id)
                    head_car.task = None

            road.cars.deltel(head_car)
            road.cars.append(head_car)

if __name__ == '__main__':
    gen = CarGenerator({"road_length": 1000, "lam": 1, "size": 1, "car_length": 3.8})
