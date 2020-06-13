import threading


class SteeringLogic(threading.Thread):
    def __init__(self, events):
        threading.Thread.__init__(self)
        self.events = events

    def run(self):
        while True:
            print(self.events.recv())
