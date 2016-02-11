#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import requests

API='http://api.fixer.io/latest'

class NotAvailableException(Exception):
    pass

def get_config_dir():
    path = os.environ.get('XDG_CONFIG_HOME')
    if path is None:
        path = os.path.expanduser('~/.config')
    path = os.path.join(path, 'currency')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def get_rates_remote(symbol, path):
    r = requests.get(API, params={'base': symbol})
    return r.json()

def get_rates_local(symbol, path):
    with open(path, 'r') as f:
        return json.load(f)

def get_rates(symbol):
    symbol = symbol.upper()
    path = os.path.join(get_config_dir(), "{}.json".format(symbol))

    rates = None
    if os.path.isfile(path):
        rates = get_rates_local(symbol, path)

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    if rates is None or rates['date'] != today:
        try:
            rates = get_rates_remote(symbol, path)
            with open(path, 'w') as f:
                json.dump(rates, f)
        except:
            pass

    if rates is None:
        raise NotAvailableException()

    return rates['rates']

def convert(n, symbol_from, symbol_to):
    rates = get_rates(symbol_from)
    rate = rates[symbol_to.upper()]

    return n * rate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts currency')
    parser.add_argument('N', help='Amount', type=float)
    parser.add_argument('FROM', help='Source currency symbol', type=str)
    parser.add_argument('TO', help='Target currency symbol (default=DKK)', type=str, default='DKK', nargs='?')
    args = parser.parse_args()

    converted = convert(args.N, args.FROM, args.TO)

    print("{0:.2f} {1:s} = {2:.2f} {3:s}".format(args.N, args.FROM.upper(), converted, args.TO.upper()))
