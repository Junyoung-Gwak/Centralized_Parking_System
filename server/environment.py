import numpy as np


class Environment:
    def __init__(self, obstacles):
        self.background = np.ones((360, 640, 3))
        self.place_obstacles(obstacles)

    def place_obstacles(self, obs):
        obstacles = np.concatenate([np.array([[0, i] for i in range(37)]),
                                    np.array([[63,i] for i in range(37)]),
                                    np.array([[i, 0] for i in range(65)]),
                                    np.array([[i,35] for i in range(65)]),
                                    obs]) * 10
        for ob in obstacles:
            self.background[ob[1]:ob[1]+10, ob[0]:ob[0]+10] = 0


class Parking:
    def __init__(self):
        self.walls = [[12, i] for i in range(26, 36)] + \
                     [[12, i] for i in range(0, 10)] + \
                     [[22, i] for i in range(26, 36)] + \
                     [[22, i] for i in range(0, 10)] + \
                     [[32, i] for i in range(26, 36)] + \
                     [[32, i] for i in range(0, 10)] + \
                     [[42, i] for i in range(26, 36)] + \
                     [[42, i] for i in range(0, 10)] + \
                     [[52, i] for i in range(26, 36)] + \
                     [[52, i] for i in range(0, 10)]
        self.obs = np.array(self.walls)
        self.cars = {1: [17, 5], 2: [27, 5], 3: [37, 5], 4: [47, 5], 5: [57, 5],
                     6: [17, 29], 7: [27, 29], 8: [37, 29], 9: [47, 29], 10: [57, 29]}

    def select_parking_index(self, car_pos):
        return self.cars[car_pos]

    def generate_obstacles(self):
        return self.obs