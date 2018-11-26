"""Normalize address"""

from __future__ import print_function

import json
import re
from time import sleep

import requests


def clean(str_):
    """Clean a string."""
    alpha = re.compile(r'\W+')
    return ' '.join([re.sub(alpha, '', x) for x in str_.split()])


def parse_countries(jfile='country.json'):
    """Parse countries."""
    with open(jfile, 'r') as file_:
        tmp = json.load(file_)
        return tmp.values()


def query(address_str):
    """Query address string."""
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address={}'.format(
        address_str)
    attempt = 1
    while attempt < 6:
        try:
            address_comps = requests.get(url).json()['results'][
                0]['address_components']
            for comp in address_comps:
                if 'country' in comp['types']:
                    return comp['long_name']
            break
        except IndexError:
            return ''
        except:
            sleep(0.5)
            attempt += 1
            continue


if __name__ == '__main__':
    ADD = query('')
    print(ADD)
    print(parse_countries())
    print(clean('   (Hong Kong) dhigadi dhau      si dh 2 1 45 6    '))
