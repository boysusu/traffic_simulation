from simulation import Simulation
from window import Window

sim = Simulation()

sim.create_roads([
    ((1000, -8.25), (0, -8.25), True),
    ((1000, -5.25), (0, -5.25)),
    ((1000, -1.75), (0, -1.75)),
    ((0, 1.75), (1000, 1.75)),
    ((0, 5.25), (1000, 5.25)),
    ((0, 8.25), (1000, 8.25), True),
])

win = Window(sim)
win.run()