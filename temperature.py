#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from datetime import datetime
import sqlite3
import threading
from sqlite3 import Error
from http.server import HTTPServer, BaseHTTPRequestHandler
from quik import FileLoader
import json

RELAY_GPIO_PIN = 21
database = "pythonsqlite.db"

DEVICE1 = "28-3c01f0957154"
DEVICE2 = "28-3c01f095d551"

#conn = sqlite3.connect(database)

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(RELAY_GPIO_PIN, GPIO.OUT)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def blink_relay():
    GPIO.output(RELAY_GPIO_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RELAY_GPIO_PIN, GPIO.LOW)

def thread_func():
    conn = sqlite3.connect(database)
    while(1):
        try:
            temp1, temp2 = tempread()
            scrie_temp_bd(conn, temp1, temp2, 0)
            print(temp)
            time.sleep(1)
        except:
            pass

def temp_min(x):
    if x < 180:
        return 15 - (22 / 180.0) * x
    elif x < 300:
        pass


def experiment_thread(iteratii=1):
    print('Am inceput experimentul')

    # Racire
    for x in range(16 * 60):
        temp = 0 # Citesti din BD

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
        temp = 0 # Citesti din BD

        if temp > temp_min(x):
            # Stinge lampile
            pass
        elif temp < temp_max(x):
            # Porneste lampile
            pass
        time.sleep(60)
  
    # Stinge lampile

def tempread():
    with open(f'/sys/devices/w1_bus_master1/{DEVICE1}/w1_slave', 'r') as f:
        words = f.read().split()
        last_word = words[-1]
        temp1 = int(last_word.split('=')[1]) / 1000

    with open(f'/sys/devices/w1_bus_master1/{DEVICE2}/w1_slave', 'r') as f:
        words = f.read().split()
        last_word = words[-1]
        temp2 = int(last_word.split('=')[1]) / 1000

    return (temp1, temp2)


def creaza_bd():
    #database = "~/pythonsqlite.db"
    conn = sqlite3.connect(database)

    sql_create_data_table = """ CREATE TABLE IF NOT EXISTS project (
                                    tempsenzor1 real NOT NULL,
                                    tempsenzor2 real NOT NULL,
                                    tempsenzor3 real NOT NULL,
                                    timp numeric NOT NULL
                                ); """
    sql_starea_releelor = """ CREATE TABLE IF NOT EXISTS relee (
                             starereleu1 integer NOT NULL,
                             starereleu2 integer NOT NULL
                          ); """

    sql_user_can_change = """
                            nr_cicluri,
                            durata_inghet,
                            durata_dezghet,
                            temp_min,
                            temp_max
                          """
    #tabel poate schimba nr ciclurilor,durata,temperaturi max/min
    conn.execute(sql_create_data_table)
    conn.execute(sql_starea_releelor)
    conn.close()

def scrie_temp_bd(conn,temp1,temp2,temp3):
    sql_write_temp = "INSERT INTO project (tempsenzor1,tempsenzor2,tempsenzor3,timp) VALUES (?,?,?,?) "
    conn.execute(sql_write_temp,(temp1,temp2,temp3,int(time.time()))) 
    conn.commit()

def citeste_temp_bd():
    conn = sqlite3.connect(database)
    now = int(time.time())
    sql_read_temp_table = "SELECT tempsenzor1,tempsenzor2,tempsenzor3,timp FROM project WHERE timp > ? - 3600"
    data = conn.execute(sql_read_temp_table, [now]).fetchall()
    conn.close()
    return data

creaza_bd();
x = threading.Thread(target=thread_func, args=())
x.start()
#while(1):
    #server si bd in the same script
    #citeste temp
    #temp = tempread()
    #print(temp)
    #scrie bd
    #time.sleep(1)

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
        temps = citeste_temp_bd()
        s = template.render({'temps': json.dumps(temps)},loader=loader).encode('utf-8')
        self.wfile.write(s)

    def send_temperatures(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # Add human-readable datetime representation
        temps = [
                list(t) + [datetime.fromtimestamp(t[3]).strftime('%c')]
                for t in citeste_temp_bd()
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


address = ('', 8080)
server = HTTPServer(address, Handler)
server.serve_forever()







