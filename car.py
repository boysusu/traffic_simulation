import numpy as np

from util.const import GHz


class Car:
    def __init__(self, config={}):
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self.init_properties()

    def set_default_config(self):
        self.id = None  # 汽车唯一id

        self.l = 3.8  # 车身长度
        self.h = 2  # 车身宽度
        self.s0 = 2  # 期望车距
        self.T = 0.1  # 驾驶员反应时间
        self.v_max = 60.0  # 正常行驶最大车速
        self.a_max = 5.0  # 最大加速度
        self.b_max = 5.0  # 非紧急制动下的最大减速度

        self.max_num_of_channels = 3  # 信道数量

        self.current_road_index = 0  # 车辆所处的车道

        self.v = 20  # 车辆的当前速率
        self.a = 0  # 车辆的当前加速度

        self.angle_cos = 1  # 车辆行驶方向与x轴的余弦值
        self.x = 0  # 车辆的x坐标
        self.y = 0  # 车辆的y坐标

        self.cpu = 1 * GHz  # 车载设备计算能力
        self.max_num_of_channels = 3  # 信道数量

    def init_properties(self):
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)

    def update(self, lead, dt):
        # 更新车辆位置和速度
        if self.v + self.a * dt < 0:  # 当dt之后速度为负值，则速度降到0的时间为t=v/a,a为负数
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.angle_cos*(self.v * dt + self.a * dt * dt / 2)

        # 更新车辆加速度
        alpha = 0
        if lead:
            delta_x = self.angle_cos*(lead.data.x - self.x) - lead.data.l  # 实际车距=两车中心点的差值-车长
            delta_v = self.v - lead.data.v

            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1 - (self.v / self.v_max) ** 4 - alpha ** 2)
