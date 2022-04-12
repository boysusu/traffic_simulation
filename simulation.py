from road import Road
from car_generator import CarGenerator
from rsu import RSU
from copy import deepcopy


class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0  # 时刻
        self.frame_count = 0  # 仿真帧计数
        self.dt = 1 / 60  # 仿真时间步长
        self.roads = []  # 存储所有车道和人行道
        self.rsus = []  # 存储所有RSU
        self.cars = []  # 存储所有汽车
        self.distance_map = None
        self.generators = []  # 车辆生成器

    def create_road(self, start, end, is_bicycle=False):
        road = Road(start, end, is_bicycle)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_rsu(self, config):
        rsu = RSU(config)
        self.rsus.append(rsu)
        return rsu

    def create_rsus(self, rsu_list):
        for rsu_config in rsu_list:
            self.create_rsu(rsu_config)

    def create_gen(self, config={}):
        gen = CarGenerator(self, config)
        car_mum = gen.generate_cars()
        self.distance_map = [[None for _ in range(car_mum)] for __ in range(car_mum)]
        self.generators.append(gen)

    def update(self):
        # Update every car road
        for road in self.roads:
            if road.is_bicycle:
                continue
            road.update(self.dt)

        for gen in self.generators:
            gen.update()

        # Increment time
        self.t += self.dt
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
