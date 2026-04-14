import RPi.GPIO as GPIO
import math
from time import sleep
from socket import *
import threading

# motor state
STOP  = 0
FORWARD  = 1
BACKWARD = 2

# motor channel
CH1 = 0
CH2 = 1

# PIN I/O config
OUTPUT = 1
INPUT = 0

# PIN Mapping
#PWM PIN
ENA = 13  #37 pin

#GPIO PIN
IN1 = 14  #37 pin
IN2 = 15  #35 pin

servoPin = 12
SERVO_MAX_DUTY = 11
SERVO_MIN_DUTY = 5

pwmA,servo = '',''
speed = 100
GPIO.setmode(GPIO.BCM)
# PIN config func
def setPinConfig(SERVO, EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    GPIO.setup(SERVO, GPIO.OUT)
    # 100khz - PWM
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    servo = GPIO.PWM(SERVO, 50)
    servo.start(0)
    return pwm, servo

# motor control func
def setMotorContorl(pwm, INA, INB, speed, stat):

    #motor velocity control PWM
    pwm.ChangeDutyCycle(speed)
    if stat == FORWARD:
        GPIO.output(INA, 1)
        GPIO.output(INB, 0)

    #BACKWORD
    elif stat == BACKWARD:
        GPIO.output(INA, 0)
        GPIO.output(INB, 1)

    #STOP
    elif stat == STOP:
        GPIO.output(INA, 0)
        GPIO.output(INB, 0)


# easy version(rapping)
def setMotor(ch, speed, stat):
        setMotorContorl(pwmA, IN1, IN2, speed, stat)

def setServoPos(servo, degree):
    if degree in range(62,75):
        degree = 30 + (degree - 62) * 3.1
    elif degree in range(75,109):
        degree = 95 + (degree - 90) * 1.67
    elif degree >= 109:
        degree = 135 + (degree - 120)
    if degree > 180:
        degree = 180
    duty = SERVO_MIN_DUTY + (degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
    print('degree: {} to {}(Duty)'.format(degree, duty))
    servo.ChangeDutyCycle(duty)

def receive(sock):
    global speed
    while True:
        commands = sock.recv(150).decode('utf-8').split(',')
        print(commands)
        for command in commands:
          if command == '':
            break
          print(command, ',')
          command = int(command)
          if command <= 2:
              setMotor(CH1, speed, command) #STOP  = 0, FORWARD  = 1, BACKWARD = 2
          elif command == 3:
              speed = 50
              setMotor(CH1, speed, 2)
              sleep(0.1)
              setMotor(CH1, speed, 0)
          elif command == 4:
              speed = 50
              setMotor(CH1, speed, 1)
              sleep(0.1)
              setMotor(CH1, speed, 0)
          elif command <= 120:
              setServoPos(servo, command)
              speed = 40+abs(90-int(command))*2
              if speed>100 : speed = 100
              pwmA.ChangeDutyCycle(speed)

port = 9000

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('192.168.0.101', port)) #webcam server IP 

receiver = threading.Thread(target=receive, args=(clientSock,))
receiver.start()


try:
    print("start")
    # GPIO 모드 설정
    #모터 핀 설정
    #핀 설정후 PWM 핸들 얻어옴 
    pwmA,servo = setPinConfig(servoPin,ENA, IN1, IN2)
    while True:
        sleep(1000000)
        pass

finally:
    setMotor(CH1, 0, 0)
    setServoPos(servo, 95)
