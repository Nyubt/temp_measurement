#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import sqlite3
from sqlite3 import Error

RELAY_GPIO_PIN = 21

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

def tempread():
    with open('/sys/devices/w1_bus_master1/28-3c01d607489b/w1_slave', 'r') as f:
        words = f.read().split()
        last_word = words[-1]
        temp_c = int(last_word.split('=')[1]) / 1000
        return temp_c

print(tempread())

def creaza_bd():
    database = "~/pythonsqlite.db"

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

creaza_bd();
while(1):
    #server si bd in the same script
    #citeste temp
    #scrie bd
    wait(1000)
