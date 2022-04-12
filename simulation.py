from road import Road
from car_generator import CarGenerator
from rsu import RSU
from scipy.spatial import distance
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
        self.V2V_distance_map = None  # 存储所有汽车之间的距离
        self.V2R_distance_map = None  # 存储汽车与RSU之间的距离
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

        # 初始化距离矩阵
        self.V2V_distance_map = [[None for _ in range(car_mum)] for __ in range(car_mum)]
        self.V2R_distance_map = [[None for _ in range(len(self.rsus))] for __ in range(car_mum)]
        self.generators.append(gen)

    def update_distance(self):
        for i in range(len(self.cars)):
            #  更新v2v距离矩阵
            for j in range(i+1, len(self.cars)):
                self.V2V_distance_map[i][j] = \
                    distance.euclidean((self.cars[i].x, self.cars[i].y), (self.cars[j].x, self.cars[j].y))
                self.V2V_distance_map[j][i] = self.V2V_distance_map[i][j]

            #  更新v2r距离矩阵
            for k in range(len(self.rsus)):
                self.V2R_distance_map[i][k] = \
                    distance.euclidean((self.cars[i].x, self.cars[i].y), (self.rsus[k].x, self.rsus[k].y))

    def update(self):
        # Update every car road
        for road in self.roads:
            if road.is_bicycle:
                continue
            road.update(self.dt)

        for gen in self.generators:
            gen.update()

        # 更新距离矩阵
        self.update_distance()
        # 更新时刻和帧数
        self.t += self.dt
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
