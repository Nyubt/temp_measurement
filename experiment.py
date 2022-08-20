from threading import Thread, Event
import time

from config import DATABASE, RASPBERRY_PI, ExperimentConfig
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
    def __init__(self, experiment: ExperimentConfig):
        self.device = DEVICE
        self.experiment = experiment
        self.stop_event = Event()
        Thread.__init__(self, daemon=True)

    def run(self):
        print("Am inceput experimentul")
        repo = Repository()

        for cycle in range(self.experiment.cycles):
            for minute in range(self.experiment.duration * 60):
                hour = minute / 60.0
                temp = repo.read_last_temp_db()
                upper_a, upper_b = 0, 0
                lower_a, lower_b = 0, 0

                for upper_segment in self.experiment.upper:
                    if upper_segment.start >= hour and upper_segment.end <= hour:
                        upper_a, upper_b = upper_segment.A, upper_segment.B
                        break

                for lower_segment in self.experiment.lower:
                    if lower_segment.start >= hour and lower_segment.end <= hour:
                        lower_a, lower_b = lower_segment.A, lower_segment.B
                        break

                temp_max = upper_a * hour + upper_b
                temp_min = lower_a * hour + lower_b

                if upper_a > 0 or (upper_a == 0 and upper_b > 0):
                    # Incalzire
                    print("Incalzire")
                    if temp > temp_min:
                        self.device.stop_heater()
                    elif temp < temp_max:
                        self.device.start_heater()
                else:
                    # Racire
                    print("Racire")
                    if temp > temp_min:
                        self.device.start_fridge()
                    elif temp < temp_max:
                        self.device.stop_fridge()

                    if self.stop_event.wait(timeout=60):
                        print("Condition signaled")
                        self.device.stop_heater()
                        self.device.stop_fridge()
                        return

        # Mark experiment as successful
        repo.end_test_db(False)
        self.device.stop_heater()

    def stop(self):
        print("Stopping experiment")
        self.stop_event.set()
