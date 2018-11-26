"""Use libpostal on address parts."""

from __future__ import print_function

from time import sleep
from urllib.parse import quote_plus

import requests

KEY_LIST = ['state', 'city', 'suburb', 'road', 'house']


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


def parse_addr(address_str):
    """Parse an address string using libpostal."""
    url = 'https://libpostal.mapzen.com/parse?address={}&format=keys'.format(
        quote_plus(address_str))
    res = requests.get(url).json()
    return res


def get_country(address_str):
    """Get the country of an address."""
    addr_parse = parse_addr(address_str)
    print(addr_parse)

    # handle country tags
    if 'country' in addr_parse.keys():
        return addr_parse['country'][0].capitalize(), 0

    # handle other tags
    query_count = 0
    for key in KEY_LIST:
        if key in addr_parse.keys():
            for item in reversed(addr_parse[key]):
                res = query(item + key)
                query_count += 1
                if res != '':
                    return res, query_count

    return '', query_count


if __name__ == '__main__':
    ADDR = 'matcon limited bramley dr vale park evesham'
    RES, COUNT = get_country(ADDR)
    print(RES)
    print(COUNT)
