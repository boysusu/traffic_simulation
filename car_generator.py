from car import Car
from numpy.random import randint, poisson


class CarGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        """Set default configuration"""
        self.road_length = 1000
        self.lam = 1
        self.size = 40
        self.car_length = 3.8

    def init_properties(self):
        self.generate_cars()

    def generate_cars(self):
        for k in range(len(self.sim.roads)):
            if self.sim.roads[k].is_bicycle:
                continue
            poisson_list = poisson(lam=self.lam, size=self.size)
            l = self.road_length / self.size - self.car_length / 2
            for i in range(self.size):
                if poisson_list[i] == 0:
                    continue
                d = l / poisson_list[i]
                for j in range(poisson_list[i]):
                    x = i * (self.road_length / self.size) + self.car_length / 2 + j * d
                    car = Car({
                        "x": round(x, 2),
                        "y": self.sim.roads[k].start[1],
                        "current_road_index": k,
                        "angle_cos": self.sim.roads[k].angle_cos,
                    })
                    if self.sim.roads[k].angle_cos == 1:
                        self.sim.roads[k].cars.add(car)
                    else:
                        self.sim.roads[k].cars.append(car)

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
            if head_car.x > self.road_length:
                head_car.x = 0
            elif head_car.x < 0:
                head_car.x = self.road_length
            road.cars.deltel(head_car)
            road.cars.append(head_car)

if __name__ == '__main__':
    gen = CarGenerator({"road_length": 1000, "lam": 1, "size": 1, "car_length": 3.8})
