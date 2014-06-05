#!/usr/bin/python

import os, sys

import StringIO
import csv

import requests
from collections import namedtuple

# chdir to the code root
os.chdir(os.path.dirname(os.path.dirname(__file__)))


# Defined a namedtuple to hold our location objects
Location = namedtuple(
    'Location',
    ['invoice_to', 'name', 'url', 'city', 'street', 'state', 'zip', 'off_prem', 'on_prem', 'last_sale']
)

# Get the CSV file
response = requests.get('https://docs.google.com/spreadsheets/d/1PJkUExk4TjMGamWA_SNSyHnhX8bPBcMAeODDYvtqWqg/export?gid=0&format=csv')
assert response.status_code == 200, 'Wrong status code'
csv_string = response.content

f = StringIO.StringIO(csv_string)
reader = csv.DictReader(f, delimiter=',')

# Parse in our locations by city
cities = {}
for row in reader:
    loc = Location(
        invoice_to= row['Invoice To'],
        name=row['Business Name'],
        url=row['URL'],
        city=row['City'],
        street=row['Street Address'],
        state=row['State'],
        zip=row['Zip'],
        off_prem=(row['Off-Prem'].lower() == 'y'),
        on_prem=(row['On-Prem'].lower() == 'y'),
        last_sale=row['Last Sale']
    )
    if (loc.off_prem):
        if loc.city not in cities:
            cities[loc.city] = []
        cities[loc.city].append(loc)

# Loop over everything and write out the file
city_names = sorted(cities.keys())
with open('_includes/locations.html', 'w') as file:
    for city in city_names:
        locations = cities[city]
        # Empty?
        if len(locations) < 1:
            continue
        # Sort
        locations.sort()
        # Print the city name to the file
        file.write('<h4>{0}</h4>\n<ul>\n'.format(city))
        # Loop through locations
        for loc in locations:
            file.write('    <li><a href="{0}">{1}</a></li>\n'.format(loc.url, loc.name))
        file.write('</ul>\n')
