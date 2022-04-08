from road import Road
from car_generator import CarGenerator
from copy import deepcopy


class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0  # Time keeping
        self.frame_count = 0  # Frame count keeping
        self.dt = 1 / 60  # Simulation time step
        self.roads = []  # Array to store roads
        self.generators = []

    def create_road(self, start, end, is_bicycle=False):
        road = Road(start, end, is_bicycle)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config={}):
        gen = CarGenerator(self, config)
        self.generators.append(gen)
        return gen

    def update(self):
        # Update every car road
        for road in self.roads:
            if road.is_bicycle:
                continue
            road.update(self.dt)

        # for gen in self.generators:
        #     gen.update()

        # Increment time
        self.t += self.dt
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
