'''
@File   :   simulation.py
@Author :   boysusu
@Desc   :   仿真系统类
'''

import math
import random
from model.road import Road
from generator.car_generator import CarGenerator
from generator.task_generator import TaskGenerator
from model.rsu import RSU
from scipy.spatial import distance
from util.const import *
from numpy import log2


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
        self.V2V_channel_bandwidth = V2V_channel_bandwidth
        self.V2R_channel_bandwidth = V2R_channel_bandwidth
        self.V2V_distance_map = None  # 存储所有汽车之间的距离
        self.V2R_distance_map = None  # 存储汽车与RSU之间的距离
        self.V2V_speed_map = None  # 存储所有汽车之间的上行链路传输数据速率
        self.V2R_speed_map = None  # 存储汽车与RSU之间的上行链路传输数据速率
        self.car_generators = []  # 车辆生成器
        self.task_generators = []  # 任务生成器
        self.has_task_car_id_set = set()  # 存在计算任务的汽车id集合
        self.cooperating_car_id_set = set()  # 正在协作的汽车节点id集合

        self.results = []  # 协同节点选择结果

        self.xlsx_name = '1.xlsx'
        self.task_release_speed = 10
        self.exit_flag = False

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

    def create_car_gen(self, config={}):
        gen = CarGenerator(self, config)
        car_mum = gen.generate_cars()

        # 初始化距离矩阵
        self.V2V_distance_map = [[None for _ in range(car_mum)] for __ in range(car_mum)]
        self.V2R_distance_map = [[None for _ in range(len(self.rsus))] for __ in range(car_mum)]

        # 初始化上传链路速率矩阵
        self.V2V_speed_map = [[None for _ in range(car_mum)] for __ in range(car_mum)]
        self.V2R_speed_map = [[None for _ in range(len(self.rsus))] for __ in range(car_mum)]

        self.car_generators.append(gen)

    def create_task_gen(self, config={}):
        gen = TaskGenerator(self, config)
        self.task_generators.append(gen)

    def update_distance(self):
        for i in range(len(self.cars)):
            #  更新v2v距离矩阵
            for j in range(i + 1, len(self.cars)):
                self.V2V_distance_map[i][j] = \
                    distance.euclidean((self.cars[i].x, self.cars[i].y), (self.cars[j].x, self.cars[j].y))
                self.V2V_distance_map[j][i] = self.V2V_distance_map[i][j]

            #  更新v2r距离矩阵
            for k in range(len(self.rsus)):
                self.V2R_distance_map[i][k] = \
                    distance.euclidean((self.cars[i].x, self.cars[i].y), (self.rsus[k].x, self.rsus[k].y))

    def update_upload_speed(self):
        def calculate(d):
            return log2(1 + (
                        car_communication_transmission_power * d ** -path_loss_factor * upload_channel_fading_factor ** 2 / gaussian_noise_power))

        for i in range(len(self.cars)):
            #  更新v2v上传速率矩阵
            for j in range(i + 1, len(self.cars)):
                self.V2V_speed_map[i][j] = \
                    self.V2V_channel_bandwidth * calculate(self.V2V_distance_map[i][j])
                self.V2V_speed_map[j][i] = self.V2V_speed_map[i][j]

            #  更新v2r上传速率矩阵
            for k in range(len(self.rsus)):
                self.V2R_speed_map[i][k] = \
                    self.V2R_channel_bandwidth * calculate(self.V2R_distance_map[i][k])

    def creat_task(self):
        for gen in self.task_generators:
            tasks = gen.generate_tasks(self.task_release_speed)
            all_car_id_set = {i for i in range(len(self.cars))}
            car_list = list(all_car_id_set - self.has_task_car_id_set - self.cooperating_car_id_set)
            choose_cars = random.sample(car_list, self.task_release_speed)
            for i in range(len(tasks)):
                self.cars[choose_cars[i]].task = tasks[i]
                self.has_task_car_id_set.add(choose_cars[i])

    def update_task(self):
        for id in list(self.has_task_car_id_set):
            if self.cars[id].task.complete_need_time <= 1:
                self.cars[id].task = None
                self.has_task_car_id_set.remove(id)
                if self.cars[id].collaborative_car_id is not None:
                    self.cooperating_car_id_set.remove(self.cars[id].collaborative_car_id)
                    self.cars[self.cars[id].collaborative_car_id].need_collaborative_car_id = None
                    self.cars[id].collaborative_car_id = None
                elif self.cars[id].collaborative_rsu_id is not None:
                    self.rsus[self.cars[id].collaborative_rsu_id].use_num_of_channels -= 1
                    self.cars[id].collaborative_rsu_id = None
            else:
                self.cars[id].task.complete_need_time -= 1

    def choose_task_node(self):
        # 更新距离矩阵
        self.update_distance()
        # 更新上传速率矩阵
        self.update_upload_speed()

        def collect_result(car_id, way, local_delay, min_delay):
            if way == 'local':
                cpu = None
                min_delay = None
                d = None
                upload_speed = None
            elif way == 'V2V':
                cpu = self.cars[self.cars[car_id].collaborative_car_id].cpu / GHz
                d = self.V2V_distance_map[car_id][self.cars[car_id].collaborative_car_id]
                upload_speed = self.V2V_speed_map[car_id][self.cars[car_id].collaborative_car_id] / Mbps
            else:
                cpu = self.rsus[self.cars[car_id].collaborative_rsu_id].cpu * 0.1 / GHz
                d = self.V2R_distance_map[car_id][self.cars[car_id].collaborative_rsu_id]
                upload_speed = self.V2R_speed_map[car_id][self.cars[car_id].collaborative_rsu_id] * 0.1 / Mbps
            data = {
                '时刻(s)': self.t,
                '本地计算能力(Ghz)': self.cars[car_id].cpu / GHz,
                '计算任务数据量(Mbit)': self.cars[car_id].task.data_size / Mbit,
                '计算任务复杂度(cycles/bit)': self.cars[car_id].task.X,
                '卸载方式': way,
                '协同节点计算能力(Ghz)': cpu,
                '任务卸载距离(m)': d,
                '上行数据传输速率(Mbps)': upload_speed,
                '本地计算处理总时延(s)': local_delay,
                '协同节点处理总时延(s)': min_delay,
            }
            self.results.append(data)

        for car_id in self.has_task_car_id_set:
            # 任务还未完成的车辆跳过节点选择
            if self.cars[car_id].task.complete_need_time is not None and self.cars[car_id].task.complete_need_time > 0:
                continue
            local_calculation_delay = self.cars[car_id].task_calculate()
            rsu_collaborative_calculation_delay = 999
            car_collaborative_calculation_delay = 999

            for collaborative_car_id in range(len(self.cars)):
                if collaborative_car_id not in self.has_task_car_id_set \
                        and collaborative_car_id not in self.cooperating_car_id_set \
                        and self.V2V_distance_map[car_id][collaborative_car_id] <= 200 \
                        and car_id != collaborative_car_id:
                    # 当汽车行驶方向不同
                    if self.cars[car_id].angle_cos != self.cars[collaborative_car_id].angle_cos:
                        if self.V2V_distance_map[car_id][collaborative_car_id] >= 100:
                            continue
                        delay = self.cars[car_id].task.data_size / self.V2V_speed_map[car_id][collaborative_car_id] \
                                + self.cars[car_id].task_calculate(cpu=self.cars[collaborative_car_id].cpu)
                        if delay < car_collaborative_calculation_delay:
                            car_collaborative_calculation_delay = delay
                            self.cars[car_id].collaborative_car_id = collaborative_car_id

            for collaborative_rsu_id in range(len(self.rsus)):
                if self.rsus[collaborative_rsu_id].use_num_of_channels \
                        <= self.rsus[collaborative_rsu_id].max_num_of_channels \
                        and self.V2R_distance_map[car_id][collaborative_rsu_id] <= 150:
                    delay = self.cars[car_id].task.data_size / (self.V2R_speed_map[car_id][collaborative_rsu_id] * 0.1) \
                            + self.cars[car_id].task_calculate(cpu=self.rsus[collaborative_rsu_id].cpu * 0.1)
                    if delay < rsu_collaborative_calculation_delay:
                        rsu_collaborative_calculation_delay = delay
                        self.cars[car_id].collaborative_rsu_id = collaborative_rsu_id

            if local_calculation_delay <= rsu_collaborative_calculation_delay:
                if local_calculation_delay <= car_collaborative_calculation_delay:
                    min_delay = local_calculation_delay
                    self.cars[car_id].collaborative_rsu_id = None
                    self.cars[car_id].collaborative_car_id = None
                    way = 'local'
                else:
                    min_delay = car_collaborative_calculation_delay
                    self.cars[car_id].collaborative_rsu_id = None
                    self.cooperating_car_id_set.add(self.cars[car_id].collaborative_car_id)
                    self.cars[self.cars[car_id].collaborative_car_id].need_collaborative_car_id = car_id
                    way = 'V2V'
            else:
                if rsu_collaborative_calculation_delay < car_collaborative_calculation_delay:
                    min_delay = rsu_collaborative_calculation_delay
                    self.cars[car_id].collaborative_car_id = None
                    self.rsus[self.cars[car_id].collaborative_rsu_id].use_num_of_channels += 1
                    way = 'V2R'
                else:
                    min_delay = car_collaborative_calculation_delay
                    self.cars[car_id].collaborative_rsu_id = None
                    self.cooperating_car_id_set.add(self.cars[car_id].collaborative_car_id)
                    self.cars[self.cars[car_id].collaborative_car_id].need_collaborative_car_id = car_id
                    way = 'V2V'

            # 收集仿真结果
            collect_result(car_id, way, local_calculation_delay, min_delay)

            # 任务完成需要的帧数 向上取整确保不为0，并且补偿1帧方便观察
            self.cars[car_id].task.complete_need_time = math.ceil(min_delay / self.dt) + 1

    def road_change(self):
        if random.randint(0,10) <= 5:
            roads = self.roads[1:-1]
            road_id = random.randint(0, 3)
            if road_id == 0:
                change_road_id = 1
            elif road_id == 1:
                change_road_id = 0
            elif road_id == 2:
                change_road_id = 3
            else:
                change_road_id = 2
            length = 0
            for car in roads[road_id].cars.ergodic:
                length += 1
            if length <= 7:
                return
            change_car_id = random.randint(3, length - 3)
            i = 0
            for car in roads[road_id].cars.ergodic:
                change_car = car.data
                if i == change_car_id:
                    break
                i += 1
            # print(change_car)
            i = 0
            for car in roads[change_road_id].cars.ergodic:
                i += 1
                if roads[change_road_id].angle_cos < 0:
                    if car.data.x + change_car.l*5 < change_car.x:
                        # print(car.data, change_car)
                        if car.getNext() is None or car.getNext().data.x > change_car.x + change_car.l*5:
                            # print(i)
                            # print(change_car.x, car.data.x, car.getNext().data)
                            change_car.y = roads[change_road_id].start[1]
                            change_car.current_road_index = change_road_id
                            roads[change_road_id].cars.insert(i, change_car)
                            roads[road_id].cars.deltel(change_car)
                            break
                if roads[change_road_id].angle_cos > 0:
                    if car.data.x + change_car.l * 4 > change_car.x:
                        # print(car.data, change_car)
                        if car.getNext() is None or car.getNext().data.x < change_car.x + change_car.l * 4:
                            # print(i)
                            # print(change_car.x, car.data.x, car.getNext().data)
                            change_car.y = roads[change_road_id].start[1]
                            change_car.current_road_index = change_road_id
                            roads[change_road_id].cars.insert(i, change_car)
                            roads[road_id].cars.deltel(change_car)
                            break



    def update(self):
        # Update every car road
        for road in self.roads:
            if road.is_bicycle:
                continue
            road.update(self.dt)

        for gen in self.car_generators:
            gen.update()

        if self.frame_count > 0 and self.frame_count % 5 == 0:
            self.road_change()
        if self.frame_count > 0 and self.frame_count % 30 == 0:
            self.creat_task()
            self.choose_task_node()
            # print(f"has_task_car_id_set:{self.has_task_car_id_set}", end=', ')
            # for id in self.has_task_car_id_set:
            #     print(f"{id}(task:{self.cars[id].task},car:{self.cars[id].collaborative_car_id}, need_car:{self.cars[id].need_collaborative_car_id}, rsu:{self.cars[id].collaborative_rsu_id})",end=',')
            # print()
            # print(f"cooperating_car_id_set:{self.cooperating_car_id_set}")
            # for id in self.cooperating_car_id_set:
            #     print(f"{id}(task:{self.cars[id].task},car:{self.cars[id].collaborative_car_id}, need_car:{self.cars[id].need_collaborative_car_id}, rsu:{self.cars[id].collaborative_rsu_id})",end=',')
            # print()

        # if self.frame_count == 60 * 100:
        #     l = pd.DataFrame(self.results)
        #     print(self.xlsx_name)
        #     l.to_excel(f"./result/{self.xlsx_name}", index=False, float_format='%.3f')
        #     self.exit_flag = True

        # 更新时刻和帧数
        self.t += self.dt
        self.frame_count += 1

        self.update_task()

    def run(self, steps):
        for _ in range(steps):
            if self.exit_flag:
                break
            self.update()
