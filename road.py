from scipy.spatial import distance
from util.dlinklist import DLinkList


class Road:
    def __init__(self, start, end, is_bicycle):
        self.start = start
        self.end = end
        self.is_bicycle = is_bicycle
        self.if_left_to_right = start[0] < end[0]
        self.cars = DLinkList()
        self.init_properties()

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])

    def update(self, dt):
        if not self.cars.length > 0:
            return

        for car in self.cars.ergodic:
            car.update(car.prev, dt)