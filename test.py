import csv
import random
import time

import psycopg2
from folium.plugins import BeautifyIcon
from geopy.distance import geodesic as GD
from welbex import config
import folium


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


def get_distance():
    # Then, load the latitude and longitude data for New York & Texas
    New_York = (40.7128, 74.0060)
    Texas = (31.9686, 99.9018)

    # At last, print the distance between two points calculated in kilo-metre
    print("The distance between New York and Texas is: ", GD(New_York, Texas).miles)


def map():
    conn = psycopg2.connect(host=config.DATABASE_INFO['host'],
                            database=config.DATABASE_INFO['database'],
                            user=config.DATABASE_INFO['user'],
                            password=config.DATABASE_INFO['password'],
                            port=config.DATABASE_INFO['port'])
    cur = conn.cursor()

    cur.execute('SELECT * FROM delivery_car')
    all_cars = cur.fetchall()

    cur.execute('SELECT * FROM delivery_location')
    all_locs = cur.fetchall()
    loc = random.choice(all_locs)
    from gmplot import gmplot

    # Указываем координаты центра карты и начальный масштаб
    gmap = gmplot.GoogleMapPlotter(loc[4], loc[5], 13)
    icon_car = BeautifyIcon(
        icon='car',
        border_color='red',
        border_width=2,
        text_color='red',
        icon_shape='circle')

    icon_city = BeautifyIcon(
        icon='box',
        border_color='green',
        border_width=2,
        text_color='green',
        icon_shape='circle')

    all_locs = {i[3]: i for i in all_locs}
    print(len(all_locs))

    for i in all_cars:
        gmap.marker(all_locs[i[2]][4], all_locs[i[2]][5], color='green', title=i[1])
        #folium.Marker(location=[all_locs[i[2]][4], all_locs[i[2]][5]], popup=i[1], tooltip=i[2], icon=icon_car).add_to(m)

    c = 1
    for i in all_locs:
        print(c)
        c += 1
        gmap.marker(all_locs[i][4], all_locs[i][5], color='red', title=all_locs[i][3])
        #folium.Marker(location=[all_locs[i][4], all_locs[i][5]], popup=i,
        #              tooltip=all_locs[i][0], icon=icon_car).add_to(m)

    gmap.draw("map.html")


map()
#map_test()