import csv
import json
import random

import psycopg2
import requests

from welbex import config


def read_locations_csv():
    conn = psycopg2.connect(host=config.DATABASE_INFO['host'],
                            database=config.DATABASE_INFO['database'],
                            user=config.DATABASE_INFO['user'],
                            password=config.DATABASE_INFO['password'],
                            port=config.DATABASE_INFO['port'])
    cur = conn.cursor()


    reader = csv.DictReader(open('uszips.csv', encoding='utf-8'), delimiter=',')
    domains = []
    for row in reader:
        try:
            domain = {}
            for key in row:
                domain[key.replace('\ufeff', '')] = row[key]

            if int(domain['zip']) >=73937:
                # domains.append(domain)
                new_loc = (domain['city'], domain['state_name'], domain['zip'], domain['lat'], domain['lng'])
                print(new_loc)
                cur.execute(
                    "INSERT INTO delivery_location(city, state, postal_code, latitude, longitude) VALUES(%s, %s, %s, %s, %s);",
                    new_loc)
                conn.commit()
        except Exception as e:
            print(e)


def create_cars():
    conn = psycopg2.connect(host=config.DATABASE_INFO['host'],
                            database=config.DATABASE_INFO['database'],
                            user=config.DATABASE_INFO['user'],
                            password=config.DATABASE_INFO['password'],
                            port=config.DATABASE_INFO['port'])
    cur = conn.cursor()

    cur.execute('SELECT * FROM delivery_location')
    locations = cur.fetchall()

    for i in range(20):
        new_car = (f'{random.randint(1000, 9999)}{random.choice(["A", "C", "D", "E", "F", "G", "H", "I", "J", "L", "Z", "X", "V", "Y", "T", "O", "P", "S"])}', random.randint(0, 1000), random.choice(locations)[3])
        cur.execute('INSERT INTO delivery_car(number, weight, location) VALUES(%s, %s, %s)', new_car)
        conn.commit()

def test():
    data = {
            'weight': 100,}
    resp = requests.post('http://localhost:8000/api/edit_cargo/2/', data=data)
    print(resp.json())


if __name__ == '__main__':
   # read_locations_csv()
    create_cars()
# map_test()
