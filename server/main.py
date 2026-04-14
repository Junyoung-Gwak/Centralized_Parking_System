import argparse, math, pickle
from socket import *
from time import *

import cv2, cvzone
import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from KeyThread import KeyThread
from Car import Car

from environment import Environment, Parking
from pathplanning import PathPlanning, interpolate_path
from screen_ui import Ui_MainWindow

# 소켓통신
HOST = '192.168.0.101'
PORT = 9000  # 수신받을 Port
# 자동주차 플레그
mode_flag = 0
parking = Parking()
obs = parking.generate_obstacles()
env = Environment(obs)
background = env.background * 255
background = background.astype(np.uint8)
park_index = 1


def change_img(img):
    h, w, byte = img.shape
    img = QImage(img, w, h, byte * w, QImage.Format_RGB888)
    return QPixmap(img)


# socket통신 data 보내는 함수
def send(cmd):
    sock.send((cmd + ',').encode(encoding='utf-8'))


# 주차 관련 Thread 클래스
class ParkingThread(QThread):
    mySignal = Signal(QPixmap, QPixmap)

    def __init__(self):
        super().__init__()
        # 주차장 스트리밍
        self.cam = cv2.VideoCapture(cv2.CAP_DSHOW + 0)
        self.cam.set(3, 640)
        self.cam.set(4, 360)
        print("주차장 웹캠 연결완료")

        # base background 설정
        _, self.background = self.cam.read()
        self.background = cv2.GaussianBlur(self.background, (5, 5), 0)
        self.background = cv2.cvtColor(self.background, cv2.COLOR_BGR2GRAY)

        # drive 순서도 변수
        self.drive_state = {'None': 0, 'fw_normal': 10, 'fw_go': 11, 'fw_back': 12, 'fw_again': 13,
                            'bw_normal': 20, 'bw_go': 21, 'bw_back': 22, 'bw_again': 23}
        self.drive_flag = self.drive_state['None']

        # drive 기어
        self.drive_gear = {'Neutral': 0, 'Drive': 1, 'Rear': 2}
        self.gear_flag = self.drive_gear['Neutral']

        # 차량 인식 색상 정보
        self.color = [(0, 0, 255), (255, 0, 0)]
        self.lower_yellow, self.upper_yellow = (35, 60, 100), (85, 200, 255)
        self.lower_blue, self.upper_blue = (75, 100, 130), (130, 200, 210)

        # 차량 그리기
        self.car = Car()
        # 차량 정방향, 차량 역방향
        self.dir_car, self.dir_car_converse = None, None
        self.len = 1  # 차량 픽셀길이(변경 필요)

        # front_x  : [0][0], front_y  : [0][1]
        # center_x : [1][0], center_y : [1][1]
        # rear_x   : [2][0], rear_y   : [2][1]
        # 차량 위치
        self.car_pos = [[50, 50], [60, 60], [70, 70]]

        # 생성된 경로 index
        self.interpolated_path = None
        # 추가된 장애물
        self.add_obs = None

        # frame당 초기화 변수
        self.collision = False  # 충돌 여부
        self.nav_idx, self.nav_x, self.nav_y = 0, 0, 0  # 생성된 경로에서 현재 목표로 하는 index, 다움 목표의 x, y좌표
        self.dis_nav, self.dir_nav, self.dir_diff = 0, 0, 0  # 다음 좌표까지의 거리, 다음 좌표까지의 방향, 현재 차량 방향과 다음 좌표 방향과의 차이

        self.before_theta = None
        
        self.reverse = None
        self.simulate = [0] * 2

    def frame_init(self):
        # 차량 뒤쪽 위치
        self.car_pos[2][0] = self.car_pos[1][0] + 2 * (self.car_pos[1][0] - self.car_pos[0][0])
        self.car_pos[2][1] = self.car_pos[1][1] + 2 * (self.car_pos[1][1] - self.car_pos[0][1])
        self.len = self.cal_dis('normal') * 2 + 1
        # 후진 전진 상관없음
        self.dir_car = self.cal_slope('normal')
        self.dir_car_converse = self.cal_slope('converse')

        # 후진주차 전진주차 나누기
        if int(self.drive_flag / 10) == 1:
            self.dis_nav = self.cal_dis('front')
            self.dir_nav = self.cal_slope('front')
            self.dir_diff = (360 + self.dir_nav - self.dir_car) % 360
        else:
            self.dis_nav = self.cal_dis('rear')
            self.dir_nav = self.cal_slope('rear')
            self.dir_diff = (360 + self.dir_nav - self.dir_car_converse) % 360

    def drive(self):
        global mode_flag
        match self.drive_flag:
            case 10:  # 목표점 도착해서 최신화 한뒤 직진인지 판단
                if self.is_emergency():
                    return
                if self.is_steering():
                    self.drive_flag = self.drive_state['fw_go']
                else:
                    self.control('back')  # 조향각 보정 + 후진 명령
                    self.drive_flag = self.drive_state['fw_back']
            # ----------------------------------------------------------------------#
            case 11:  # fw_go 핸들 틀고 직진중인 상태
                if self.is_emergency():
                    return

                if self.gear_flag != self.drive_gear['Drive']:
                    send('1')
                    self.gear_flag = self.drive_gear['Drive']

                after_theta = self.cal_direction()
                if abs(self.before_theta - after_theta) > 5:
                    self.control('go')

                if self.is_collision():
                    send('3')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.control('back')  # 조향각 보정 + 후진 명령
                    self.drive_flag = self.drive_state['fw_back']

                elif self.is_arrived():
                    self.gear_flag = self.drive_gear['Neutral']
                    self.next_point()
                    if self.nav_idx == len(self.interpolated_path):
                        send('3')
                        self.nav_idx = 0
                        mode_flag = 0
                        self.drive_flag = self.drive_state['None']
                        self.interpolated_path = None
                    else:
                        self.drive_flag = self.drive_state['fw_normal']

                elif self.is_pass_away():
                    send('3')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.control('back')  # 조향각 보정 + 후진 명령
                    self.drive_flag = self.drive_state['fw_back']

            # ----------------------------------------------------------------------#
            case 12:  # fw_back 직진 못해서 빠구중
                if self.is_emergency():
                    return

                if self.gear_flag != self.drive_gear['Rear']:
                    send('2')
                    self.gear_flag = self.drive_gear['Rear']

                after_theta = self.cal_direction()
                if abs(self.before_theta - after_theta) > 5:
                    self.control('back')

                if self.is_collision():
                    send('4')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.control('go')
                    self.drive_flag = self.drive_state['fw_again']
                elif self.is_forwardable():  # 다음 점에 갈 수 있을 때까지 후진한면서 각도 계산
                    send('4')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.drive_flag = self.drive_state['fw_normal']
            # ----------------------------------------------------------------------#
            case 13:  # fw_again 후진중에 박을까봐 직진중
                if self.is_emergency():
                    return

                if self.gear_flag != self.drive_gear['Drive']:
                    send('1')
                    self.gear_flag = self.drive_gear['Drive']

                after_theta = self.cal_direction()
                if abs(self.before_theta - after_theta) > 5:
                    self.control('go')

                if not self.is_collision() and not self.is_pass_away():
                    pass

                send('3')
                self.gear_flag = self.drive_gear['Neutral']
                self.control('back')
                self.drive_flag = self.drive_state['fw_back']

            # ----------------------------------------------------------------------#
            case 20:  # 목표점 도착해서 최신화 한뒤 후진인지 판단
                if self.is_emergency():
                    return

                if self.is_steering():
                    self.drive_flag = self.drive_state['bw_go']
                else:
                    self.control('go')  # 보류 #조향각 보정 + 후진 명령
                    self.drive_flag = self.drive_state['bw_back']
            # ----------------------------------------------------------------------#
            case 21:
                if self.is_emergency():
                    return

                if self.gear_flag != self.drive_gear['Rear']:
                    send('2')
                    self.gear_flag = self.drive_gear['Rear']

                after_theta = self.cal_direction()
                if abs(self.before_theta - after_theta) > 5:
                    self.control('back')

                if self.is_collision():
                    send('4')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.control('go')  # 조향각 보정 + 전진 명령
                    self.drive_flag = self.drive_state['bw_back']

                elif self.is_arrived():
                    self.gear_flag = self.drive_gear['Neutral']
                    self.next_point()
                    if self.nav_idx == len(self.interpolated_path):
                        send('4')
                        self.nav_idx = 0
                        mode_flag = 0
                        self.drive_flag = self.drive_state['None']
                        self.interpolated_path = None
                    else:
                        self.drive_flag = self.drive_state['bw_normal']

                elif self.is_pass_away():
                    send('4')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.control('go')  # 조향각 보정 + 후진 명령
                    self.drive_flag = self.drive_state['bw_back']

            # ----------------------------------------------------------------------#
            case 22:
                if self.is_emergency():
                    return

                if self.gear_flag != self.drive_gear['Drive']:
                    send('1')
                    self.gear_flag = self.drive_gear['Drive']

                after_theta = self.cal_direction()
                if abs(self.before_theta - after_theta) > 5:
                    self.control('go')

                if self.is_collision():
                    send('3')
                    self.gear_flag = self.drive_gear['Neutral']
                    self.control('go')
                    self.drive_flag = self.drive_state['bw_again']
                elif self.is_forwardable():  # 다음 점에 갈 수 있을 때까지 후진한면서 각도 계산
                    send('3')
                    print("forward")
                    self.gear_flag = self.drive_gear['Neutral']
                    self.drive_flag = self.drive_state['bw_go']
            # ----------------------------------------------------------------------#
            case 23:
                if self.is_emergency():
                    return

                if self.gear_flag != self.drive_gear['Rear']:
                    send('2')
                    self.gear_flag = self.drive_gear['Rear']

                after_theta = self.cal_direction()
                if abs(self.before_theta - after_theta) > 5:
                    self.control('back')

                if not self.is_collision() and not self.is_pass_away():
                    pass

                send('4')
                self.gear_flag = self.drive_gear['Neutral']
                self.control('go')
                self.drive_flag = self.drive_state['bw_back']

    # 다음 위치 확인
    def next_point(self):
        self.nav_idx += 1
        if self.interpolated_path is not None and self.nav_idx < len(self.interpolated_path):
            self.nav_y = self.interpolated_path[self.nav_idx][1]
            self.nav_x = self.interpolated_path[self.nav_idx][0]

    # 목표점을 가기 위한 휠 조향각 계산
    def cal_direction(self):
        # 차량방향 기준 조향각
        if self.gear_flag != self.drive_gear['Rear']:
            # temp = 직선 dir_car 에서 점 nav_y, nav_x 까지의 거리
            temp = abs(self.nav_y - self.car_pos[0][1] - math.tan(math.radians(self.dir_car)) *
                         (self.nav_x - self.car_pos[0][0])) / math.sqrt(1 + math.tan(math.radians(self.dir_car)) ** 2)
            data = math.atan(temp / (math.sqrt(self.dis_nav ** 2 - temp ** 2) + self.dis_nav ** 2 / (2 * self.len)))
        else:
            # 후진 계산을 위한 차량 반전
            rx = self.car_pos[1][0] + 3 * (self.car_pos[1][0] - self.car_pos[0][0])
            ry = self.car_pos[1][1] + 3 * (self.car_pos[1][1] - self.car_pos[0][1])
            temp = abs(self.nav_y - ry - math.tan(math.radians(self.dir_car_converse)) *
                         (self.nav_x - rx)) / math.sqrt(1 + math.tan(math.radians(self.dir_car_converse)) ** 2)
            data = 1.29 * math.atan(temp / (math.sqrt(self.dis_nav ** 2 - temp ** 2) + self.dis_nav ** 2 / (2 * self.len)))
        return int(math.degrees(math.atan(data)))

    # 전,후진 명령을 내리는 함수
    def control(self, dir):
        theta = self.cal_direction()
        self.before_theta = theta
        # 내각, 외각 보정(후진용)
        num = -1 if dir == 'go' else 1
        dir_wheel = max(63, int(90 + theta * (-1 if self.dir_diff < 180 else 1) * num))
        dir_wheel = str(min(120, dir_wheel))
        send(dir_wheel)

    # 조향 가능 여부 체크 함수
    def is_steering(self):
        if self.is_pass_away():
            return False

        theta = self.cal_direction()
        self.before_theta = theta
        # 내각, 외각 보정
        num = 1 if self.dir_diff < 180 else -1
        dir_wheel = int(90 + theta * (1 if int(self.drive_flag / 10) == 1 else -1) * num)

        # 조향 가능여부
        if 60 <= dir_wheel <= 120:
            send(str(dir_wheel))
            return True
        return False

    # 상태 확인 함수들
    def is_emergency(self):
        flag = False
        for i in range(self.nav_idx, len(self.interpolated_path)):
            if not np.all(self.simulate[0][int(self.interpolated_path[i][1])][int(self.interpolated_path[i][0])] == 0):
                flag = True
                break
        if flag:
            send('0')
            self.gear_flag = self.drive_gear['Neutral']
            self.drive_flag = self.drive_state['fw_normal'] if int(self.drive_flag / 10) == 1 else self.drive_state['bw_normal']
            return True
        return False

    # 충돌 체크 여부 함수
    def is_collision(self):
        if self.collision:
            # 장애물과 차량이 생긴 뒤의 장애물의 모양을 비교
            if np.array_equal(self.reverse, self.simulate[0]):
                self.collision = False
        else:
            if not np.array_equal(self.reverse, self.simulate[0]):
                self.collision = True
                return True
        return False

    # 목표점을 지나갔는지 확인하는 함수
    def is_pass_away(self):
        return True if 90 <= self.dir_diff <= 270 else False

    # 목표점 도착 여부 체크 확인
    def is_arrived(self):
        if int(self.drive_flag / 10) == 1:
            return True if self.dis_nav < max(self.len / 3, 10) else False
        if self.interpolated_path is not None and self.nav_idx > len(self.interpolated_path) - 2:
            if self.dis_nav < self.len / 5:
                return True
        else:
            if self.dis_nav < max(self.len / 3, 22):
                return True
        return False

    # 이동 가능한지 체크하는 함수
    def is_forwardable(self):
        num = 30 if int(self.drive_flag / 10) == 1 else 42
        return True if min(360 - self.dir_diff, self.dir_diff) < num else False

    # 기울기 계산 함수
    def cal_slope(self, state):
        slope = {'front': math.atan2((self.nav_y - self.car_pos[0][1]), (self.nav_x - self.car_pos[0][0])),
                 'rear': math.atan2((self.nav_y - self.car_pos[2][1]), (self.nav_x - self.car_pos[2][0])),
                 'normal': math.atan2((self.car_pos[0][1] - self.car_pos[1][1]), (self.car_pos[0][0] - self.car_pos[1][0])),
                 'converse': math.atan2((self.car_pos[2][1] - self.car_pos[1][1]), (self.car_pos[2][0] - self.car_pos[1][0])),
                 'check': math.atan2((self.nav_y - self.car_pos[1][1]), (self.nav_x - self.car_pos[1][0]))}
        return math.degrees(slope[state]) + 180

    # 거리 계산 함수
    def cal_dis(self, num):
        dis = {'front': math.sqrt((self.nav_x - self.car_pos[0][0]) ** 2 + (self.nav_y - self.car_pos[0][1]) ** 2),
               'rear': math.sqrt((self.nav_x - self.car_pos[2][0]) ** 2 + (self.nav_y - self.car_pos[2][1]) ** 2),
               'normal': math.sqrt((self.car_pos[0][0] - self.car_pos[1][0]) ** 2 + (self.car_pos[0][1] - self.car_pos[1][1]) ** 2)}
        return dis[num]

    def run(self):
        while True:
            ok, img = self.cam.read()
            if not ok:
                break
            self.print_image(img)

    def make_path(self, img, x, y):
        parser = argparse.ArgumentParser()  # 초기 데이터
        parser.add_argument('--x_start', type=int, default=x, help='X of start')
        parser.add_argument('--y_start', type=int, default=y, help='Y of start')
        parser.add_argument('--x_end', type=int, default=64, help='X of end')
        parser.add_argument('--y_end', type=int, default=36, help='Y of end')
        parser.add_argument('--parking', type=int, default=park_index, help='park position in parking1 out of 24')
        args = parser.parse_args()

        start = np.array([args.x_start, args.y_start])  # 차 시작점
        end = parking.select_parking_index(args.parking)  # 목적지를 입력

        path_planner = PathPlanning(obs, start, self.add_obs)
        # 시작점부터 도착점까지 경로 생성
        path = path_planner.plan_path(int(start[0]), int(start[1]), int(end[0]), int(end[1]))
        path = interpolate_path(path, sample_rate=2)
        self.interpolated_path = []  # 경로 초기화
        if path[-1][1] < 60:
            path[-1][1] = 40
        elif path[-1][1] > 280:
            path[-1][1] = 310
        # 생성된 경로의 간격 변경
        for i in range(5, len(path), 5):
            self.interpolated_path.append(path[i])
        self.interpolated_path.append(path[-1])
        return self.draw_path(img, self.interpolated_path, 0)

    # 화면에 경로 그리기
    def draw_path(self, img, path, st):
        for i in range(st, len(path)):
            cv2.circle(img, (int(path[i][0]), int(path[i][1])), 2, (0, 0, 0), -1)
        return img

    def print_image(self, img):
        global mode_flag
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HSV로 변환
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # 범위 값으로 HSV 이미지에서 마스크를 생성합니다.
        img_mask = [cv2.inRange(img_hsv, self.lower_yellow, self.upper_yellow),
                    cv2.inRange(img_hsv, self.lower_blue, self.upper_blue)]
        for i in range(0, 2):
            img_mask[i] = cv2.morphologyEx(img_mask[i], cv2.MORPH_DILATE, kernel, iterations=3)
            # 라벨링
            nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_mask[i])
            MAX = -1
            max_index = -1
            for j in range(nlabels):
                if j < 1:
                    continue
                area = stats[j, cv2.CC_STAT_AREA]
                if area > MAX:
                    MAX = area
                    max_index = j
            if max_index != -1:
                self.car_pos[i][0] = int(centroids[max_index, 0])
                self.car_pos[i][1] = int(centroids[max_index, 1])
                cv2.circle(img, (self.car_pos[i][0], self.car_pos[i][1]), 5, self.color[i], -1)

        cv2.line(img, (self.car_pos[0][0], self.car_pos[0][1]), (self.car_pos[1][0], self.car_pos[1][1]), (255, 255, 255), 2)

        blur_img = cv2.GaussianBlur(img, (5, 5), 0)
        self.simulate[0] = np.zeros((360, 640, 3))
        car = np.ones((360, 640, 3))
        car *= 255

        img_gray = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(self.background, img_gray)

        ret, diff = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY_INV)
        contours, hierachy = cv2.findContours(diff, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 500 < area < 5000:
                # maxcontours의 각 꼭지점 다각선 만들기
                hull = cv2.convexHull(cnt)
                obs = np.ones((360, 640, 3))
                obs = cv2.drawContours(obs, [hull], 0, (0, 0, 0), -1)
                # 생성된 장애물이 차인지 아닌지 판별
                if np.all(obs[self.car_pos[0][1]][self.car_pos[0][0]] < 1):
                    # car = cv2.drawContours(car, [hull], 0, (0, 0, 0), -1)
                    car = cv2.drawContours(car, [hull], 0, (0, 0, 0), 25)
                    cv2.drawContours(img, [hull], 0, (255, 0, 0), 10)
                else:
                    cv2.drawContours(img, [hull], 0, (0, 255, 0), 2)
                    self.simulate[0] = cv2.drawContours(self.simulate[0], [hull], 0, (255, 255, 255), -1)
                    self.simulate[0] = cv2.drawContours(self.simulate[0], [hull], 0, (255, 255, 255), 10)
        img = cv2.bitwise_and(background, img)
        self.simulate[0] = self.simulate[0].astype(np.uint8)
        self.simulate[1] = ~self.simulate[0]
        car = car.astype(np.uint8)
        self.simulate[1] = cv2.bitwise_and(background, self.simulate[1])
        white = np.ones((360, 640, 3))
        white *= 255
        white = white.astype(np.uint8)
        self.reverse = cv2.bitwise_xor(white, car)
        self.reverse = cv2.bitwise_or(self.reverse, self.simulate[1])

        self.frame_init()

        # 목표점 최신화
        if mode_flag:
            # 경로 재탐색 or 첫 경로 탐색
            if self.nav_idx == 0 or mode_flag == 2:
                self.add_obs = self.simulate[0]
                img = self.make_path(img, int(self.car_pos[1][0] / 10), int(self.car_pos[1][1] / 10))
                self.nav_idx = 3
                self.nav_y = self.interpolated_path[self.nav_idx][1]
                self.nav_x = self.interpolated_path[self.nav_idx][0]
                mode_flag = 1
            dir_center_nav = self.cal_slope('check')
            self.frame_init()
            if self.drive_flag == self.drive_state['None']:
                if 90 <= (360 + dir_center_nav - self.dir_car) % 360 <= 270:
                    self.drive_flag = self.drive_state['bw_normal']
                else:
                    self.drive_flag = self.drive_state['fw_normal']
            self.drive()

        # ------------그림 그리기------------#
        if self.interpolated_path is not None:
            img = self.draw_path(img, self.interpolated_path, self.nav_idx)
            self.simulate[0] = self.draw_path(self.simulate[0], self.interpolated_path, self.nav_idx)
        car_img = self.car.render(self.car_pos[0][0], self.car_pos[0][1], self.dir_car, 0)
        self.reverse = cv2.bitwise_and(self.reverse, background)
        self.reverse = cv2.bitwise_and(self.reverse, car_img)

        self.mySignal.emit(change_img(cv2.resize(img, (800, 450))), change_img(cv2.resize(self.reverse, (800, 450))))


class CheckAvailableParkinglotThread(QThread):
    mySignal = Signal(QPixmap)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(cv2.CAP_DSHOW + 0)
        self.cam.set(3, 640)
        self.cam.set(4, 360)
        print("주차장 웹캠 연결완료")

        with open('CarParkPos', 'rb') as f:
            self.pos_list = pickle.load(f)
        self.width, self.height = 85, 85

    def run(self):
        while True:
            if self.cam.get(cv2.CAP_PROP_POS_FRAMES) == self.cam.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, img = self.cam.read()
            if ret:
                self.print_image(img)

    def print_image(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.int8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        img = self.check_parking_space(img_dilate, img)
        img = cv2.bitwise_and(background, img)
        img = cv2.resize(img, (800, 450))

        self.mySignal.emit(change_img(img))

    def check_parking_space(self, img_pro, img):
        global park_index
        temp_index = 10
        space_counter = 0

        for pos in self.pos_list:
            x, y, num = pos
            num += 1
            img_crop = img_pro[y:y + self.height, x:x + self.width]
            count = cv2.countNonZero(img_crop)
            cvzone.putTextRect(img, str(num), (x, y + self.height - 5), scale=1.2,
                               thickness=1, offset=0, colorR=(0, 0, 255))

            if count < 500:
                color = (0, 255, 0)
                space_counter += 1
                if temp_index > num:
                    temp_index = num
                    park_index = temp_index
            else:
                color = (0, 0, 255)
            cv2.rectangle(img, (pos[0], pos[1]), (pos[0] + self.width, pos[1] + self.height), color, 3)

        cvzone.putTextRect(img, f'Free:{space_counter}/{len(self.pos_list)}', (50, 50), scale=2,
                           thickness=1, offset=0, colorR=(0, 200, 0))
        return img


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.thread = [None] * 3
        self.setupUi(self)
        self.main()

    # 동영상 출력
    def main(self):
        self.thread[0] = ParkingThread()
        self.thread[0].mySignal.connect(self.set_image)
        self.thread[1] = CheckAvailableParkinglotThread()
        self.thread[1].mySignal.connect(self.set_image2)
        self.thread[2] = KeyThread(sock)
        send("90")

    def set_image(self, img, img2):
        self.real_img.setPixmap(img)
        self.virtual_img.setPixmap(img2)

    def set_image2(self, img):
        self.check_free_space.setPixmap(img)

    def closeEvent(self, event):
        for th in self.thread:
            th.terminate()
            th.wait(3000)
        self.close()

    # 버튼 동작들 함수
    def start_act(self):
        for th in self.thread:
            th.start()
        print("start")

    def auto_parking_act(self):
        global mode_flag
        print("start auto parking")
        mode_flag = 1

    def refind_path_act(self):
        global mode_flag
        print("refind path")
        mode_flag = 2

# PORT
server_sock = socket(AF_INET, SOCK_STREAM)  # TCP Socket
server_sock.bind((HOST, PORT))  # 소켓에 수신받을 IP주소와 PORT를 설정
server_sock.listen(1)  # 소켓 연결, 여기서 파라미터는 접속수를 의미
print("포트 대기중입니다")
sock, addr = server_sock.accept()  # 해당 소켓을 열고 대기
sock.setblocking(True)
print("포트 접속 완료")

app = QApplication()
win = MyApp()
win.show()
app.exec()

while True:
    sleep(1)