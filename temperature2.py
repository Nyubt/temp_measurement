#!/usr/bin/env python3

import json
from quik import FileLoader
from http.server import HTTPServer, BaseHTTPRequestHandler
from sqlite3 import Error
import threading
import sqlite3
from datetime import datetime
import time
RASPBERRY_PI = False
EXPERIMENT = {
    '1': {'max': 1, 'min': 4},
    '2': {'max': 2, 'min': 3}
}

if RASPBERRY_PI:
    import RPi.GPIO as GPIO

RELAY_GPIO_PIN = 21
database = "pythonsqlite.db"

DEVICE1 = "28-3c01f0957154"
DEVICE2 = "28-3c01f095d551"

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(RELAY_GPIO_PIN, GPIO.OUT)


class DBConnection:
    def __init__(self, database):
        self.database = database

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
        sql_write_temp = "INSERT INTO temperature (temp1,temp2,temp3,read_time) VALUES (?,?,?,?) "
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
        sql_read_temp_table = "SELECT temp1,temp2,temp3,read_time FROM temperature ORDER BY read_time DESC LIMIT 1"
        data = conn.execute(sql_read_temp_table, [now]).fetchall()
        conn.close()
        return data


def blink_relay():
    GPIO.output(RELAY_GPIO_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RELAY_GPIO_PIN, GPIO.LOW)


def thread_func():
    dbconn = DBConnection(database)
    conn = dbconn.connect_db()
    while(1):
        try:
            temp1, temp2 = tempread()
            dbconn.write_temp_db(conn, temp1, temp2, 0)
            print(temp1, temp2)
        except Exception as e:
            print(e)
            pass
        time.sleep(1)


def temp_min(x):
    if x < 180:
        return 15 - (22 / 180.0) * x
    elif x < 300:
        pass


def temp_max(x):
    pass


def experiment_thread(iteratii=1):
    print('Am inceput experimentul')

    # Racire
    for x in range(16 * 60):
        temp = 0  # Citesti din BD

        if temp > temp_min(x):
            # Porneste racirea
            pass
        elif temp < temp_max(x):
            # Stinge racirea
            pass
        time.sleep(60)
    # Stinge racirea

    # Incalzire
    for x in range(16 * 60, 24 * 60):
        temp = 0  # Citesti din BD

        if temp > temp_min(x):
            # Stinge lampile
            pass
        elif temp < temp_max(x):
            # Porneste lampile
            pass
        time.sleep(60)

    # Stinge lampile


def tempread():
    if not RASPBERRY_PI:
        # temp aleatoare
        return (15, 14)

    with open(f'/sys/devices/w1_bus_master1/{DEVICE1}/w1_slave', 'r') as f:
        words = f.read().split()
        last_word = words[-1]
        temp1 = int(last_word.split('=')[1]) / 1000

    with open(f'/sys/devices/w1_bus_master1/{DEVICE2}/w1_slave', 'r') as f:
        words = f.read().split()
        last_word = words[-1]
        temp2 = int(last_word.split('=')[1]) / 1000

    return (temp1, temp2)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/temps':
            self.send_temperatures()
        else:
            self.send_html_page()

    def send_html_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        loader = FileLoader('.')
        template = loader.load_template('home.html')
        temps = dbconn.read_temp_db()
        s = template.render({'temps': json.dumps(temps)},
                            loader=loader).encode('utf-8')
        self.wfile.write(s)

    def send_temperatures(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # Add human-readable datetime representation
        temps = [
            list(t) + [datetime.fromtimestamp(t[3]).strftime('%c')]
            for t in dbconn.read_temp_db()
        ]
        self.wfile.write(bytes(json.dumps(temps), 'utf-8'))

    def do_POST(self):
        # Porneste ciclul de temperatura
        # intr-un thread nou
        # Porneste frigiderul
        # Citeste temperatura pina nu ajunge la nivelul stabilit
        # Opreste frigiderul
        print('Got request')
        content_length = int(self.headers['Content-Length'])
        print(self.headers)
        params = self.rfile.read(content_length).decode('utf-8')

        map = {}
        for keyval in params.split('&'):
            key, val = keyval.split('=')
            map[key] = val
        print(map)

        x = threading.Thread(target=experiment_thread, kwargs=map)
        x.start()

        self.send_response(200)
        self.end_headers()

        with open('home.html') as f:
            self.wfile.write(bytes(f.read(), 'utf-8'))


dbconn = DBConnection(database)
dbconn.create_db()
x = threading.Thread(target=thread_func, args=())
x.start()

address = ('', 8081)
server = HTTPServer(address, Handler)
server.serve_forever()
