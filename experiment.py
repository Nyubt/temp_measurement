from threading import Thread
import time

from config import DATABASE, RASPBERRY_PI
from device import DEVICE
from repository import Repository

# if RASPBERRY_PI:
#     import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(RELAY_GPIO_PIN, GPIO.OUT)


# def blink_relay():
#     GPIO.output(RELAY_GPIO_PIN, GPIO.HIGH)
#     time.sleep(1)
#     GPIO.output(RELAY_GPIO_PIN, GPIO.LOW)


class Experiment(Thread):
    def __init__(self):
        self.device = DEVICE
        Thread.__init__(self, daemon=True)

    def temp_min(self, x):
        if x < 180:
            return 15 - (22 / 180.0) * x
        elif x < 300:
            return 10

    def temp_max(self, x):
        return 17

    def run(self):
        print("Am inceput experimentul")
        repo = Repository()

        # Racire
        for x in range(16 * 60):
            temp = repo.read_last_temp_db()

            if temp > self.temp_min(x):
                self.device.start_fridge()
            elif temp < self.temp_max(x):
                self.device.stop_fridge()
            time.sleep(60)
        self.device.stop_fridge()

        # Incalzire
        for x in range(16 * 60, 24 * 60):
            temp = repo.read_last_temp_db()

            if temp > self.temp_min(x):
                self.device.stop_heater()
            elif temp < self.temp_max(x):
                self.device.start_heater()
            time.sleep(60)

        self.device.stop_heater()
