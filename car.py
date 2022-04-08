import numpy as np


class Car:
    def __init__(self, config={}):
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self.init_properties()

    def set_default_config(self):
        self.l = 3.8  # 车身长度
        self.h = 2  # 车身宽度
        self.s0 = 4  # 期望车距
        self.T = 1  # 驾驶员反应时间
        self.v_max = 50.0  # 正常行驶最大车速
        self.a_max = 8.0  # 最大加速度
        self.b_max = 10.0  # 非紧急制动下的最大减速度

        self.current_road_index = 0  # 车辆所处的车道

        self.x = 0  # 车辆的x轴坐标
        self.v = self.v_max  # 车辆的当前速率
        self.a = 0  # 车辆的当前加速度

    def init_properties(self):
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)

    def update(self, lead, dt):
        # 更新车辆位置和速度
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2

        # 更新车辆加速度
        alpha = 0
        if lead:
            delta_x = lead.data.x - self.x - lead.data.l
            delta_v = self.v - lead.data.v

            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1 - (self.v / self.v_max) ** 4 - alpha ** 2)
