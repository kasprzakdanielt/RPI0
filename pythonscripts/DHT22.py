import Adafruit_DHT


class Dht22(object):
    humidity_round = 4
    temperature_round = 4

    def __init__(self, humidity_round=4, temperature_round=4):
        self.humidity_round = humidity_round
        self.temperature_round = temperature_round

    def read_humidity(self):
        humidity, temperature = Adafruit_DHT.read_retry(22, 4)
        return round(humidity, self.humidity_round)

    def read_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(22, 4)
        return round(temperature, self.temperature_round)
