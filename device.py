from random import random
from typing import Tuple
from config import DEVICE1, DEVICE2, DEVICE3, RASPBERRY_PI

PIN_HEATER = 22
PIN_FRIDGE = 27
PIN_FAN = 17


if RASPBERRY_PI:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_HEATER, GPIO.IN)
    GPIO.setup(PIN_FRIDGE, GPIO.IN)
    GPIO.setup(PIN_FAN, GPIO.IN)


class TestDevice:
    temp1 = 20
    temp2 = 21
    temp3 = 22
    fridge_on = False
    heater_on = False

    def __init__(self) -> None:
        pass

    def start_heater(self):
        print("Am pornit incalzirea")
        self.heater_on = True

    def stop_heater(self):
        print("Am oprit incalzirea")
        self.heater_on = False

    def start_fridge(self):
        print("Am pornit racirea")
        self.fridge_on = True

    def stop_fridge(self):
        print("Am oprit racirea")
        self.fridge_on = False

    def start_fan(self):
        print("Am pornit ventilatorul")

    def stop_fan(self):
        print("Am oprit ventilatorul")

    def tempread(self) -> Tuple[float, float, float]:
        # temp aleatoare
        delta = 0.1 * (random() - 0.3)
        if self.heater_on:
            delta = 0.1 * random()
        elif self.fridge_on:
            delta = -0.1 * random()
        self.temp1 += delta
        self.temp2 += delta
        self.temp3 += delta

        return (self.temp1, self.temp2, self.temp3)


class RaspberryDevice:
    def __init__(self) -> None:
        pass

    def start_heater(self):
        self.stop_fridge()
        print("Starting heater")
        GPIO.setup(PIN_HEATER, GPIO.OUT)
        GPIO.output(PIN_HEATER, GPIO.HIGH)

    def stop_heater(self):
        print("Stopping heater")
        GPIO.setup(PIN_HEATER, GPIO.IN)

    def start_fridge(self):
        self.stop_heater()
        print("Starting fridge")
        GPIO.setup(PIN_FRIDGE, GPIO.OUT)
        GPIO.output(PIN_FRIDGE, GPIO.HIGH)

    def stop_fridge(self):
        print("Stopping fridge")
        GPIO.setup(PIN_FRIDGE, GPIO.IN)

    def start_fan(self):
        print("Starting fan")
        GPIO.setup(PIN_FAN, GPIO.OUT)
        GPIO.output(PIN_FAN, GPIO.HIGH)

    def stop_fan(self):
        print("Stopping fan")
        GPIO.setup(PIN_FAN, GPIO.IN)

    def tempread(self) -> Tuple[float, float, float]:
        with open(f"/sys/devices/w1_bus_master1/{DEVICE1}/w1_slave", "r") as f:
            words = f.read().split()
            last_word = words[-1]
            temp1 = int(last_word.split("=")[1]) / 1000.0

        with open(f"/sys/devices/w1_bus_master1/{DEVICE2}/w1_slave", "r") as f:
            words = f.read().split()
            last_word = words[-1]
            temp2 = int(last_word.split("=")[1]) / 1000.0

        with open(f"/sys/devices/w1_bus_master1/{DEVICE3}/w1_slave", "r") as f:
            words = f.read().split()
            last_word = words[-1]
            temp3 = int(last_word.split("=")[1]) / 1000.0

        return (temp1, temp2, temp3)


if not RASPBERRY_PI:
    DEVICE = TestDevice()
else:
    DEVICE = RaspberryDevice()
