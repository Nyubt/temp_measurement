#!/usr/bin/env python3

import signal
import sys
from http.server import HTTPServer

from handler import Handler
from repository import Repository
from temperature import Temperature


def signal_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

dbconn = Repository()
dbconn.create_db()

temp_read = Temperature()
temp_read.start()

address = ("", 8081)
server = HTTPServer(address, Handler)
server.serve_forever()
