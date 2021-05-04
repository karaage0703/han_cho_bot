from pymycobot.mycobot import MyCobot
import time

DEVICE_NAME = '/dev/tty.usbserial-0203B064'
mycobot = MyCobot(DEVICE_NAME)


mycobot.send_radians([0.0, 0.0, 0.0, 1.3, 0.0, 0.0], 30)
buffer = input('input any key: ')
mycobot.send_radians([0.0, -0.9, 2.18, 0.17, 0.0, 0.0], 30)
time.sleep(2)
mycobot.send_radians([2.9, -0.9, 2.18, 0.17, 0.0, 0.0], 30)
time.sleep(2)
mycobot.send_radians([2.9, 1.3, 1.5, -1.4, 0.0, 0.0], 30)
time.sleep(3)
mycobot.send_radians([2.9, 1.3, 1.5, -1.4, -1.57, 0.0], 90)
