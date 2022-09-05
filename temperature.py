from threading import Thread
import time
import experiment
import handler
import traceback

from repository import Repository
from config import DATABASE, RASPBERRY_PI, DEVICE1, DEVICE2
from device import DEVICE


class Temperature(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)

    def run(self):
        dbconn = Repository()
        conn = dbconn.connect_db()
        f = open("temperature.txt", "a")
        while 1:
            try:
                temp1, temp2, temp3 = DEVICE.tempread()
                if not handler.experiment:
                    dbconn.write_temp_db(conn, temp1, temp2, temp3, 0, 0)
                else:
                    dbconn.write_temp_db(
                        conn,
                        temp1,
                        temp2,
                        temp3,
                        handler.experiment.temp_min,
                        handler.experiment.temp_max,
                    )
                    f.write(f"{temp1},{temp2},{temp3},{int(time.time())}\n")
                    f.flush()
                print(temp1, temp2, temp3)
            except Exception as e:
                print(e)
                # traceback.print_exc()
                pass
            time.sleep(60)
