import queue
from multiprocessing import Pipe

import SteeringLogic
import XboxOneController
from OLEDDisplay import OLEDDisplay, readInput

if __name__ == '__main__':
    queue = queue.Queue()
    parent_conn, child_conn = Pipe()
    xbox = XboxOneController.XboxOneController(parent_conn)
    oled = OLEDDisplay()
    steering_logic = SteeringLogic.SteeringLogic(child_conn)
    inp = readInput()
    oled.start()
    inp.start()
    xbox.start()
    steering_logic.start()
    steering_logic.join()
    oled.join()
    inp.join()
    xbox.join()
