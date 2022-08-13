### Start solution here
import requests
import pandas as pd
import time
import os

response = requests.get('https://api.coinbase.com/v2/currencies')
currencies = {}
for row in response.json()['data']:
    currencies[row['id']] = row['name']


def get_currency(currency_code):
    print(currency_code, currencies[currency_code])


def get_currency_exchange_rates(currency_code):
    response = requests.get('https://api.coinbase.com/v2/exchange-rates', params={'currency': currency_code})
    result = pd.DataFrame(response.json()['data']['rates'].items(), columns=['currency_code', 'exchange_rate'])
    print(result)
    result['base_currency_code'] = currency_code
    result['base_currency'] = currencies[currency_code]
    result['currency'] = result['currency_code'].replace(currencies)
    if not os.path.isdir('Output'):
        os.mkdir('Output')
    result.to_csv(f'Output/{currency_code}-exchange_output.{time.time()}.csv', index=False, columns=['base_currency_code', 'base_currency', 'currency_code', 'currency', 'exchange_rate'])


def get_price(currency_code):
    print("""Choose operation:
    b - buy
    s - sell
    t - spot price""")
    option = input()
    response = requests.get(f'https://api.coinbase.com/v2/prices/BTC-{currency_code}/{options_price[option]}')
    print(response.json()['data']['amount'])


options_dict = {'c': get_currency, 'e': get_currency_exchange_rates, 'p': get_price}
options_price = {'b': 'buy', 's': 'sell', 't': 'spot'}

while True:
    print("""Choose an option:
    c - currency name
    e - currency exchange rates
    p - price for exchange operation
    any other option - quit""")
    option = input()
    if option in options_dict:
        print('Enter currency code:')
        code = input().upper()
        options_dict[option](code)
    else:
        break
