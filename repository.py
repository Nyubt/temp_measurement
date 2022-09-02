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
                                 cycles integer NOT NULL,
                                 experiment_id integer NOT NULL,
                                 time_start integer NOT NULL,
                                 time_end integer,
                                 terminated bool NOT NULL default false
                              ); """

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

    def start_test_db(self, cycles, experiment):
        conn = self.connect_db()
        sql_write_test = (
            "INSERT INTO test (cycles, experiment_id, time_start) VALUES (?,?,?) "
        )
        conn.execute(sql_write_test, (cycles, experiment, int(time.time())))
        conn.commit()
        conn.close()

    def end_test_db(self, terminated):
        conn = self.connect_db()
        sql_get_last_test_table = """SELECT exp_id FROM test where time_end is null order by time_start desc limit 1"""
        data = conn.execute(sql_get_last_test_table, []).fetchone()
        sql_end_test = "UPDATE test set terminated=?, time_end=? where exp_id=? "
        conn.execute(sql_end_test, (terminated, int(time.time()), data[0]))
        conn.commit()
        conn.close()

    def read_temp_db(self):
        conn = self.connect_db()
        now = int(time.time())
        sql_time_start = """select time_start from test where time_end is null order by time_start desc limit 1"""
        data = conn.execute(sql_read_temp_table, []).fetchall()
        if len(data) == 0:
            sql_read_temp_table = """SELECT temp1,temp2,temp3,read_time FROM temperature 
            WHERE read_time"""
        else:
            sql_read_temp_table = """SELECT temp1,temp2,temp3,read_time FROM temperature 
            WHERE read_time > (select time_start from test where time_end is null order by time_start desc limit 1)"""
        data = conn.execute(sql_read_temp_table, []).fetchall()
        conn.close()
        return data

    def read_test_db(self):
        conn = self.connect_db()
        sql_read_temp_table = """SELECT time_start,time_end,terminated FROM test """
        data = conn.execute(sql_read_temp_table, []).fetchall()
        conn.close()
        return data

    def read_last_temp_db(self):
        conn = self.connect_db()
        now = int(time.time())
        sql_read_temp_table = "SELECT (temp1 + temp2 + temp3)/3 FROM temperature ORDER BY read_time DESC LIMIT 1"
        data = conn.execute(sql_read_temp_table, []).fetchone()
        conn.close()
        return data[0]
