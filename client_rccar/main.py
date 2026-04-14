import pigpio
from time import sleep

pi = pigpio.pi()
pi.set_mode(4, pigpio.OUTPUT)
while True:
    print('1')
    pi.set_servo_pulsewidth(4, 0)
    sleep(1)

    pi.set_servo_pulsewidth(4, 500)
    sleep(1)

    pi.set_servo_pulsewidth(4, 1500)  # 가운데로 이동 90도
    sleep(1)

    pi.set_servo_pulsewidth(4, 2500)  # 180도 끝으로 이동.
    sleep(1)
