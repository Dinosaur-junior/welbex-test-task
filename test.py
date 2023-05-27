import csv
import json

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

            # domains.append(domain)
            new_loc = (domain['city'], domain['state_name'], domain['zip'], domain['lat'], domain['lng'])
            print(new_loc)
            cur.execute(
                "INSERT INTO delivery_location(city, state, postal_code, latitude, longitude) VALUES(%s, %s, %s, %s, %s);",
                new_loc)
            conn.commit()
        except Exception as e:
            print(e)


def test():
    data = {
            'weight': 100,}
    resp = requests.post('http://localhost:8000/api/edit_cargo/2/', data=data)
    print(resp.json())


if __name__ == '__main__':
    read_locations_csv()
# map_test()
