import numpy as np
import math
import scipy.interpolate as scipy_interpolate


def interpolate_b_spline_path(x, y, n_path_points, degree=3):
    x_len = len(x)
    ipl_t = np.linspace(0.0, x_len - 1, x_len)
    spl_i_x = scipy_interpolate.make_interp_spline(ipl_t, x, k=degree)
    spl_i_y = scipy_interpolate.make_interp_spline(ipl_t, y, k=degree)
    travel = np.linspace(0.0, x_len - 1, n_path_points)
    return spl_i_x(travel), spl_i_y(travel)


def interpolate_path(path, sample_rate):
    path_len = len(path)
    choices = np.arange(0, path_len, sample_rate)
    if path_len - 1 not in choices:
        choices = np.append(choices, path_len - 1)
    way_point_x = path[choices, 0]
    way_point_y = path[choices, 1]
    n_course_point = path_len * 3
    try:
        rix, riy = interpolate_b_spline_path(way_point_x, way_point_y, n_course_point)
        new_path = np.vstack([rix * 10, riy * 10]).T
        return new_path
    except:
        return np.vstack([0,0]).T


def angle_of_line(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


class AStarPlanner:
    def __init__(self, ox, oy, resolution, rr, start, add_obs):
        """
        Initialize grid map for a star planning

        ox: x position list of Obstacles [m]
        oy: y position list of Obstacles [m]
        resolution: grid resolution [m]
        rr: robot radius[m]
        """
        self.resolution = resolution
        self.rr = rr
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.obstacle_map = None
        self.x_width, self.y_width = 0, 0
        self.motion = self.get_motion_model()
        self.calc_obstacle_map(ox, oy, start, add_obs)

    class Node:
        def __init__(self, x, y, cost, parent_index):
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent_index = parent_index

        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(
                self.cost) + "," + str(self.parent_index)

    def planning(self, sx, sy, gx, gy):
        """
        A star path search

        input:
            s_x: start x position [m]
            s_y: start y position [m]
            gx: goal x position [m]
            gy: goal y position [m]

        output:
            rx: x position list of the final path
            ry: y position list of the final path
        """

        start_node = self.Node(self.calc_xy_index(sx, self.min_x),
                               self.calc_xy_index(sy, self.min_y), 0.0, -1)
        goal_node = self.Node(self.calc_xy_index(gx, self.min_x),
                              self.calc_xy_index(gy, self.min_y), 0.0, -1)
        open_set, closed_set = dict(), dict()
        open_set[self.calc_grid_index(start_node)] = start_node

        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            c_id = min(open_set, key=lambda o: open_set[o].cost + self.calc_heuristic(goal_node, open_set[o]))
            current = open_set[c_id]

            if current.x == goal_node.x and current.y == goal_node.y:
                print("Find goal")
                goal_node.parent_index = current.parent_index
                goal_node.cost = current.cost
                break

            # Remove the item from the open set
            del open_set[c_id]

            # Add it to the closed set
            closed_set[c_id] = current

            # expand_grid search grid based on motion model
            # weight = [3, 2, 1]
            diff = abs(18 - current.y)
            for i, _ in enumerate(self.motion):
                weight = 0 if diff == 18 else 1
                node = self.Node(current.x + self.motion[i][0], current.y + self.motion[i][1], current.cost + self.motion[i][2] + weight * diff, c_id)
                n_id = self.calc_grid_index(node)

                # If the node is not safe, do nothing
                if not self.verify_node(node):
                    continue

                if n_id in closed_set:
                    continue

                if n_id not in open_set:
                    open_set[n_id] = node  # discovered a new node
                else:
                    if open_set[n_id].cost > node.cost:
                        # This path is the best until now. record it
                        open_set[n_id] = node

        rx, ry = self.calc_final_path(goal_node, closed_set)

        return rx, ry

    def calc_final_path(self, goal_node, closed_set):
        # generate final course
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)]
        parent_index = goal_node.parent_index
        while parent_index != -1:
            n = closed_set[parent_index]
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            parent_index = n.parent_index

        return rx, ry

    @staticmethod
    def calc_heuristic(n1, n2):
        w = 1.0  # weight of heuristic
        return w * math.hypot(n1.x - n2.x, n1.y - n2.y)

    def calc_grid_position(self, index, min_position):
        """
        calc grid position

        :param index:
        :param min_position:
        :return:
        """
        return index * self.resolution + min_position

    def calc_xy_index(self, position, min_pos):
        return round((position - min_pos) / self.resolution)

    def calc_grid_index(self, node):
        return (node.y - self.min_y) * self.x_width + (node.x - self.min_x)

    def verify_node(self, node):
        px = self.calc_grid_position(node.x, self.min_x)
        py = self.calc_grid_position(node.y, self.min_y)

        if self.max_x <= px < self.min_x or self.max_y <= py < self.min_y:
            return False

        # print(self.obstacle_map)
        # collision check
        try:
            if self.obstacle_map[node.x][node.y]:
                return False
        except:
            return False
        return True

    def calc_obstacle_map(self, ox, oy, start, add_obs):
        self.min_x, self.min_y = round(min(ox)), round(min(oy))
        self.max_x, self.max_y = round(max(ox)), round(max(oy))
        self.x_width, self.y_width = round((self.max_x - self.min_x) / self.resolution), round((self.max_y - self.min_y) / self.resolution)

        add_ox = []
        add_oy = []

        for ix in range(self.x_width):
            for iy in range(self.y_width):
                if iy < self.y_width and ix < self.x_width and np.all(add_obs[iy * 10][ix * 10] > 240):
                    add_ox.append(ix)
                    add_oy.append(iy)

        # obstacle map generation
        self.obstacle_map = [[False for _ in range(self.y_width)] for _ in range(self.x_width)]
        for ix in range(self.x_width):
            x = self.calc_grid_position(ix, self.min_x)
            for iy in range(self.y_width):
                y = self.calc_grid_position(iy, self.min_y)
                for iox, ioy in zip(ox, oy):
                    d = math.hypot(iox - x, ioy - y)
                    d2 = math.hypot(start[0] - x, start[1] - y)
                    if d2 > self.rr > d or (iox == x and ioy == y):
                        self.obstacle_map[ix][iy] = True
                        break
                for iox, ioy in zip(add_ox, add_oy):
                    d = math.hypot(iox - x, ioy - y)
                    d2 = math.hypot(start[0] - x, start[1] - y)
                    if d2 > self.rr - 1 > d or (iox == x and ioy == y):
                        self.obstacle_map[ix][iy] = True
                        break

    @staticmethod
    def get_motion_model():
        # dx, dy, cost
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                  [-1, -1, math.sqrt(2)],
                  [-1, 1, math.sqrt(2)],
                  [1, -1, math.sqrt(2)],
                  [1, 1, math.sqrt(2)],
                  [2, 1, math.sqrt(5)],
                  [2, -1, math.sqrt(5)],
                  [-2, 1, math.sqrt(5)],
                  [-2, -1, math.sqrt(5)],
                  [1, 2, math.sqrt(5)],
                  [1, -2, math.sqrt(5)],
                  [-1, 2, math.sqrt(5)],
                  [-1, -2, math.sqrt(5)]]
        return motion


# 경로 계획
class PathPlanning:
    def __init__(self, obstacles, start, add):
        self.margin = 1
        # sacale obstacles from env margin to pathplanning margin
        obstacles = obstacles + np.array([self.margin, self.margin])
        obstacles = obstacles[(obstacles[:, 0] >= 0) & (obstacles[:, 1] >= 0)]

        self.obs = np.concatenate([np.array([[0, i] for i in range(34 + 2 * self.margin)]),
                                   np.array([[62 + 2 * self.margin - 1, i] for i in range(34 + 2 * self.margin)]),
                                   np.array([[i, 0] for i in range(62 + 2 * self.margin)]),
                                   np.array([[i, 34 + 2 * self.margin - 1] for i in range(62 + 2 * self.margin)]),
                                   obstacles])

        self.ox = [int(item) for item in self.obs[:, 0]]
        self.oy = [int(item) for item in self.obs[:, 1]]
        self.grid_size = 1

        # 그리드 사이즈?
        self.robot_radius = 5  # 회전반경?
        self.a_star = AStarPlanner(self.ox, self.oy, self.grid_size, self.robot_radius, start, add)

    def plan_path(self, sx, sy, gx, gy):
        rx, ry = self.a_star.planning(sx + self.margin, sy + self.margin, gx + self.margin, gy + self.margin)
        rx = np.array(rx) - self.margin + 0.5
        ry = np.array(ry) - self.margin + 0.5
        path = np.vstack([rx, ry]).T
        return path[::-1]
