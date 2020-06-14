import queue
from multiprocessing import Pipe

import SteeringLogic
import XboxOneController
from ArduinioCommunication import ArduinoCommunication
# from OLEDDisplay import OLEDDisplay

if __name__ == '__main__':
    queue = queue.Queue()
    parent_conn, child_conn = Pipe()
    xbox = XboxOneController.XboxOneController(parent_conn)
    # oled = OLEDDisplay()
    steering_logic = SteeringLogic.SteeringLogic(child_conn, queue)
    comms = ArduinoCommunication(queue)
    # oled.start()
    xbox.start()
    steering_logic.start()
    comms.start()
    print("Ready...")
    steering_logic.join()
    # oled.join()
    xbox.join()
    comms.join()
