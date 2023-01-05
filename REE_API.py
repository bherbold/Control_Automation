# import requests library
import requests
import json
# import plotting library
#import matplotlib
#import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

#Helper Functions
from HelperFunc import handle_response_code

def get_real_price_now ():
    # datetime object containing current date and time
    now = datetime.now()
    # Time formate for REE API
    dt_string_start = now.strftime("%Y/%m/%dT%H:00")
    endhour = now + timedelta(hours=1)
    dt_string_end = endhour.strftime("%Y/%m/%dT%H:00")
    #print("date and time =", dt_string)

    endpoint = 'https://apidatos.ree.es'
    get_archives = '/en/datos/mercados/precios-mercados-tiempo-real'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Host': 'apidatos.ree.es'}
    params = {'start_date': dt_string_start, 'end_date': dt_string_end, 'time_trunc': 'hour'}

    response = requests.get(endpoint + get_archives, headers=headers, params=params)

    handle_response_code(response)

    json = response.json()

    spot_market_prices = json['included'][0]
    values = spot_market_prices['attributes']['values']
    print(values[0]['value'])

def get_real_price_day ():
    # datetime object containing current date and time


    now = datetime.now()


    # Time formate for REE API
    nowZero = now - timedelta(hours=now.hour)
    dt_string_start = nowZero.strftime("%Y/%m/%dT%00:00")
    endhour = nowZero + timedelta(hours=23)
    dt_string_end = endhour.strftime("%Y/%m/%dT%H:00")
    #print("date and time =", dt_string)

    endpoint = 'https://apidatos.ree.es'
    get_archives = '/en/datos/mercados/precios-mercados-tiempo-real'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Host': 'apidatos.ree.es'}
    params = {'start_date': dt_string_start, 'end_date': dt_string_end, 'time_trunc': 'hour'}

    response = requests.get(endpoint + get_archives, headers=headers, params=params)

    handle_response_code(response)

    json = response.json()

    spot_market_prices = json['included'][0]
    values = spot_market_prices['attributes']['values']
    print(values)
#get_real_price_now ()
#get_real_price_day ()

def calCosts (demand_kw,priceData,priceDeltahour):
    """

    :param demand_kw: Demand in KW
    :param priceData: Array from API with each hour as an entry (should be 24 entries)
    :param priceDeltahour: 15 min = 1/4 , 10min = 1/6 ...
    :return: Price to pay
    """
    now = datetime.now()

    price = 0;

    for value in priceData:

        if(value['datetime'] == now):

            price = value['value']
    return price * demand_kw * priceDeltahour