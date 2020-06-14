import threading


class SteeringLogic(threading.Thread):
    left_blinkers = 0
    servo_angle = 90

    def __init__(self, events, queue):
        threading.Thread.__init__(self)
        self.events = events
        self.queue = queue
        print("SteeringLogic has been initialized")

    def run(self):
        while True:
            to_be_sent = ""
            incoming_data = self.events.recv()
            if incoming_data["A"] == 1:
                if self.left_blinkers == 0:
                    self.left_blinkers = 1
                    to_be_sent += "1"
                else:
                    self.left_blinkers = 0
                    to_be_sent += "0"
            else:
                to_be_sent += str(self.left_blinkers)
            self.servo_angle = int((incoming_data["XAXIS"]*45)+90)
            to_be_sent += "," + str(self.servo_angle)
            self.queue.put_nowait(to_be_sent)