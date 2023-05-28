# -*- coding: utf-8 -*-
# Written by Dinosaur
#                __
#               / _)
#      _.----._/ /
#     /         /
#  __/ (  | (  |
# /__.-'|_|--|_|


# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import random
import time
from threading import Thread

import psycopg2

from welbex import config

# ---------------------------------------------------------------------------------------------------------------------
# configuration

# connect to the database
conn = psycopg2.connect(host=config.DATABASE_INFO['host'],
                        database=config.DATABASE_INFO['database'],
                        user=config.DATABASE_INFO['user'],
                        password=config.DATABASE_INFO['password'],
                        port=config.DATABASE_INFO['port'])
cur = conn.cursor()


# ---------------------------------------------------------------------------------------------------------------------
class CarsMovement(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                cur.execute('SELECT * FROM delivery_car')
                cars = cur.fetchall()

                cur.execute('SELECT * FROM delivery_location')
                locations = cur.fetchall()

                for car in cars:
                    loc = random.choice(locations)
                    cur.execute('UPDATE delivery_car SET location=%s WHERE id=%s', (loc[3], car[0]))
                    conn.commit()

            except Exception as e:
                print(e)
            time.sleep(5)


# ---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    cars_movement_app = CarsMovement()
    cars_movement_app.start()
