import csv

def read_locations_csv():
    reader = csv.DictReader(open('uszips.csv', encoding='utf-8'), delimiter=',')
    domains = []
    for row in reader:
        try:
            domain = {}
            for key in row:
                domain[key.replace('\ufeff', '')] = row[key]

            domains.append(domain)
            print(domain)
        except Exception as e:
            print(e)

