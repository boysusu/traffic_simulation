from car import Car
from numpy.random import randint,poisson


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
        for road in self.sim.roads:
            if road.is_bicycle:
                continue
            poisson_list = poisson(lam=self.lam, size=self.size)
            l = self.road_length/self.size - self.car_length/2
            for i in range(self.size):
                if poisson_list[i] == 0:
                    continue
                d = l / poisson_list[i]
                for j in range(poisson_list[i]):
                    x = i * (self.road_length/self.size) + self.car_length/2 + j*d
                    road.cars.add(Car({"x": round(x, 2)}))

            # for car in road.cars.ergodic:
            #     print(car.data.x,end=',')
            # print()



    # def update(self):
    #     """Add vehicles"""
    #     if self.sim.t - self.last_added_time >= 60 / self.vehicle_rate:
    #         # If time elasped after last added vehicle is
    #         # greater than vehicle_period; generate a vehicle
    #         road = self.sim.roads[self.upcoming_vehicle.path[0]]
    #         if len(road.vehicles) == 0\
    #            or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.l:
    #             # If there is space for the generated vehicle; add it
    #             self.upcoming_vehicle.time_added = self.sim.t
    #             road.vehicles.append(self.upcoming_vehicle)
    #             # Reset last_added_time and upcoming_vehicle
    #             self.last_added_time = self.sim.t
    #         self.upcoming_vehicle = self.generate_vehicle()

if __name__ == '__main__':
    gen = CarGenerator({"road_length":1000, "lam":1, "size":40, "car_length":3.8})


