import cv2
import pickle
from environment import Environment, Parking
import numpy as np

width, height = 85, 85
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 360)
state = 0
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
        num = len(posList)
except:
    posList = []
    num =0

def mouseClick(events,x,y,flags,params):
    global num
    if events == cv2.EVENT_LBUTTONDOWN: #왼쪽 버튼 클릭
        posList.append((x, y, num,state))
        num += 1
    if events == cv2.EVENT_RBUTTONDOWN and num > 0: #오른쪽 버튼 클릭
        for i, pos in enumerate(posList):
            x1, y1 = pos[0],pos[1]
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                num -= 1

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


parking1 = Parking()
obs = parking1.generate_obstacles()
env = Environment(obs)
background = env.background * 255
background = background.astype(np.uint8)

while True:
    success, img = cam.read()
    if not success:
        break
    print(img.dtype, background.dtype)
    cv2.bitwise_and(background, img, img)
    # img = cv2.resize(img, (800, 450))

    for pos in posList :
        cv2.rectangle(img, [pos[0],pos[1]], (pos[0] + width, pos[1] + height), (255, 0, 255), 3)
    print(num)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)
