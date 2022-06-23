from threading import Thread
import time

from repository import Repository
from config import DATABASE, RASPBERRY_PI, DEVICE1, DEVICE2
from device import DEVICE


class Temperature(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)

    def run(self):
        dbconn = Repository()
        conn = dbconn.connect_db()
        while 1:
            try:
                temp1, temp2 = DEVICE.tempread()
                dbconn.write_temp_db(conn, temp1, temp2, 0)
                # print(temp1, temp2)
            except Exception as e:
                print(e)
                pass
            time.sleep(1)
