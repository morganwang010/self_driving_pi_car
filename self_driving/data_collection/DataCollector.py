import sys
import os
import inspect
import keyboard as key
import nxt
from util import get_date

almost_current = os.path.abspath(inspect.getfile(inspect.currentframe()))
currentdir = os.path.dirname(almost_current)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from nxt_car import bluetooth
from vision.cam import getCamera

class DataCollector(object):
    """
    to do
    """
    def __init__(self, name=""):
        sock, brick = bluetooth.connectCar()
        self.leftMotor = nxt.Motor(brick, nxt.PORT_B)
        self.rightMotor = nxt.Motor(brick, nxt.PORT_A)
        turn_ratio = 0
        self.both = nxt.SynchronizedMotors(self.leftMotor,
                                      self.rightMotor,
                                      turn_ratio)
        self.dir_name = name + get_date()
        os.makedir(self.dir_name)
        self.data_dict = {}
        self.count = 0

        self.camera = getCamera()

    @staticmethod
    def saveImage(folder, name, frame):
        name += ".png"
        path = os.path.join(folder, name)
        cv2.imwrite(path, frame)

    def saveDict(self, cmd):
        self.data_dict[str(self.count)] = cmd
        self.count += 1


    def generate(self):
        while True:
            _, im = self.camera.read()
            try:
                if key.is_pressed('q'):
                    print('Exiting...')
                    break

                elif key.is_pressed('up'):
                    self.both.run(40)
                    self.saveImage(self.dir_name, str(self.count),im)
                    self.saveDict('up')
                    time.sleep(0.05)

                elif key.is_pressed('down'):
                    self.both.run(-40)
                    self.saveImage(self.dir_name, str(self.count),im)
                    self.saveDict('down')
                    time.sleep(0.05)

                elif key.is_pressed('left'):
                    self.rightMotor.weak_turn(40,30)
                    self.leftMotor.weak_turn(-40,30)
                    self.saveImage(self.dir_name, str(self.count),im)
                    self.saveDict('left')

                elif key.is_pressed('right'):
                    self.rightMotor.weak_turn(-40,30)
                    self.leftMotor.weak_turn(40,30)
                    self.saveImage(self.dir_name, str(self.count),im)
                    self.saveDict('right')

                # elif key.is_pressed('space'):
                #     self.leftMotor.idle()
                #     self.rightMotor.idle()
                #     self.leftMotor.brake()
                #     self.rightMotor.brake()
                #     print('stopping...')

                else:
                    self.leftMotor.idle()
                    self.rightMotor.idle()
            except:
                break
