#!/usr/bin/python

import StringIO
import csv

import requests

response = requests.get('https://docs.google.com/spreadsheets/d/1PJkUExk4TjMGamWA_SNSyHnhX8bPBcMAeODDYvtqWqg/export?gid=0&format=csv')
assert response.status_code == 200, 'Wrong status code'
csv_string = response.content

f = StringIO.StringIO(csv_string)
reader = csv.DictReader(f, delimiter=',')
for row in reader:
    print repr(row)

# @todo sort the data
# @todo print it out to jekyl templates
