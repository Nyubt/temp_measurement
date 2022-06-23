import sqlite3
import time

from config import DATABASE


class Repository:
    def __init__(self):
        self.database = DATABASE

    def connect_db(self):
        conn = sqlite3.connect(self.database)
        return conn

    def create_db(self):
        conn = self.connect_db()

        sql_create_temperature_data_table = """ CREATE TABLE IF NOT EXISTS temperature (
                                        temp1 real NOT NULL,
                                        temp2 real NOT NULL,
                                        temp3 real NOT NULL,
                                        read_time numeric NOT NULL
                                    ); """

        sql_create_test_data_table = """ CREATE TABLE IF NOT EXISTS test (
                                 exp_id integer PRIMARY KEY AUTOINCREMENT,
                                 time_start integer NOT NULL,
                                 time_end integer,
                                 terminated bool NOT NULL
                              ); """

        sql_user_can_change = """
                                nr_cicluri,
                                experimentul
                              """
        # tabel poate schimba nr ciclurilor,durata,temperaturi max/min
        conn.execute(sql_create_temperature_data_table)
        conn.execute(sql_create_test_data_table)
        conn.close()

    def write_temp_db(self, conn, temp1, temp2, temp3):
        sql_write_temp = (
            "INSERT INTO temperature (temp1,temp2,temp3,read_time) VALUES (?,?,?,?) "
        )
        conn.execute(sql_write_temp, (temp1, temp2, temp3, int(time.time())))
        conn.commit()

    def read_temp_db(self):
        conn = self.connect_db()
        now = int(time.time())
        sql_read_temp_table = "SELECT temp1,temp2,temp3,read_time FROM temperature WHERE read_time > ? - 3600"
        data = conn.execute(sql_read_temp_table, [now]).fetchall()
        conn.close()
        return data

    def read_last_temp_db(self):
        conn = self.connect_db()
        now = int(time.time())
        sql_read_temp_table = "SELECT temp1,temp2,temp3,read_time FROM temperature ORDER BY read_time DESC LIMIT 1"
        data = conn.execute(sql_read_temp_table, []).fetchone()
        conn.close()
        return data[0]