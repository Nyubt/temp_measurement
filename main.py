#!/usr/bin/env python3

import signal
import sys
from http.server import HTTPServer

from handler import Handler
from repository import Repository
from temperature import Temperature
from config import RASPBERRY_PI


def signal_handler(sig, frame):
    if RASPBERRY_PI:
        import RPi.GPIO as GPIO
        GPIO.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

dbconn = Repository()
dbconn.create_db()

temp_read = Temperature()
temp_read.start()

address = ("", 8081)
print('Listening on', address)
server = HTTPServer(address, Handler)
server.serve_forever()
