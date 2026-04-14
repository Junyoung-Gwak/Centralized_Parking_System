import cv2
import math
import numpy as np


class Car:
    def __init__(self):
        self.car_length = 50
        self.car_width = 25
        self.car_color = np.array([255, 0, 0]) / 255
        self.car_struct = np.array([[+self.car_length / 2, +self.car_width / 2],
                                    [+self.car_length / 2, -self.car_width / 2],
                                    [-self.car_length / 2, -self.car_width / 2],
                                    [-self.car_length / 2, +self.car_width / 2]],
                                   np.int32)
        # 바퀴 변수
        self.wheel_length = 11.25
        self.wheel_width = 5.25
        self.wheel_positions = np.array([[18.75, 11.25], [18.75, -11.25], [-18.75, 11.25], [-18.75, -11.25]])
        self.wheel_color = np.array([20, 20, 20]) / 255
        self.wheel_struct = np.array([[+self.wheel_length / 2, +self.wheel_width / 2],
                                      [+self.wheel_length / 2, -self.wheel_width / 2],
                                      [-self.wheel_length / 2, -self.wheel_width / 2],
                                      [-self.wheel_length / 2, +self.wheel_width / 2]],
                                     np.int32)

        # 헤드라이트 변수
        self.light_length = 5
        self.light_width = 11
        self.light_positions = np.array([[-30, 12], [-30, -12]])
        self.light_color = np.array([0, 0, 255]) / 255
        self.light_struct = np.array([[+self.light_length / 2, +self.light_width / 2],
                                      [+self.light_length / 2, -self.light_width / 2],
                                      [-self.light_length / 2, -self.light_width / 2],
                                      [-self.light_length / 2, +self.light_width / 2]],
                                     np.int32)

    def rotate_car(self, pts, angle=0):
        R = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]])
        return ((R @ pts.T).T).astype(int)

    def render(self, x, y, psi, delta):
        # 각도 변환
        psi = math.radians(psi)
        car = np.ones((360, 640, 3))

        # 차량 바디 그리기
        rotated_struct = self.rotate_car(self.car_struct, angle=psi)
        rotated_struct += np.array([x, y])
        cv2.fillPoly(car, [rotated_struct], self.car_color)

        # 바퀴 그리기
        rotated_wheel_center = self.rotate_car(self.wheel_positions, angle=psi)
        for i, wheel in enumerate(rotated_wheel_center):
            if i < 2:
                rotated_wheel = self.rotate_car(self.wheel_struct, angle=delta + psi)
            else:
                rotated_wheel = self.rotate_car(self.wheel_struct, angle=psi)
            rotated_wheel += np.array([x, y]) + wheel
            cv2.fillPoly(car, [rotated_wheel], self.wheel_color)

        # 라이트 그리기
        rotated_light_center = self.rotate_car(self.light_positions, angle=psi)
        for i, light in enumerate(rotated_light_center):
            rotated_light = self.rotate_car(self.light_struct, angle=psi)
            rotated_light += np.array([x, y]) + light
            cv2.fillPoly(car, [rotated_light], self.light_color)

        return (car * 255).astype(np.uint8)
