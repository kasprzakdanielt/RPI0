import datetime
import threading

import pygame


class XboxOneController(threading.Thread):
    t0 = datetime.time()
    controls = {
        "A": 0,
        "B": 0,
        "X": 0,
        "Y": 0,
        "XAXIS": 0.0,
        "LT": -1.0,
        "RT": -1.0
    }

    def __init__(self, pipe):
        threading.Thread.__init__(self)
        pipe.send(self.controls)
        self.queue = pipe
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print("XboxOneController has been initialized")

    def run(self):
        while True:
            pygame.event.wait()
            self.controls["B"] = self.joystick.get_button(1)
            self.controls["A"] = self.joystick.get_button(0)
            self.controls["X"] = self.joystick.get_button(3)
            self.controls["Y"] = self.joystick.get_button(4)
            self.controls["XAXIS"] = self.joystick.get_axis(0)
            self.controls["LT"] = self.joystick.get_axis(5)
            self.controls["RT"] = self.joystick.get_axis(4)
            self.queue.send(self.controls)
