from random import random
from typing import Tuple
from config import DEVICE1, DEVICE2, RASPBERRY_PI


class TestDevice:
    temp1 = 20
    temp2 = 21
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

    def tempread(self) -> Tuple[float, float]:
        # temp aleatoare
        delta = 0.1 * (random() - 0.5)
        if self.heater_on:
            delta = 0.1 * random()
        elif self.fridge_on:
            delta = -0.1 * random()
        self.temp1 += delta
        self.temp2 += delta

        return (self.temp1, self.temp2)


class RaspberryDevice:
    def __init__(self) -> None:
        pass

    def start_heater(self):
        # TODO: Implement me
        pass

    def stop_heater(self):
        # TODO: Implement me
        pass

    def start_fridge(self):
        # TODO: Implement me
        pass

    def stop_fridge(self):
        # TODO: Implement me
        pass

    def tempread(self) -> Tuple[float, float]:
        with open(f"/sys/devices/w1_bus_master1/{DEVICE1}/w1_slave", "r") as f:
            words = f.read().split()
            last_word = words[-1]
            temp1 = int(last_word.split("=")[1]) / 1000

        with open(f"/sys/devices/w1_bus_master1/{DEVICE2}/w1_slave", "r") as f:
            words = f.read().split()
            last_word = words[-1]
            temp2 = int(last_word.split("=")[1]) / 1000

        return (temp1, temp2)


DEVICE = TestDevice()
