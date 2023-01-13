# import requests library
import requests
# import plotting library
#import matplotlib
#import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Helper Functions
from Data_Management.HelperFunc import handle_response_code

def get_real_price_now ():
    """

    :return: Price for this hour in EURO per KWH
    """
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
    #print(values[0]['value'])
    return values[0]['value']/1000 # 1/1000 for price per KWH

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

    for t in values:
        t['datetime'] = datetime.fromisoformat(t['datetime'])

    #print(values)
    return values
#get_real_price_now ()
#pr = get_real_price_day ()

def calCosts (demand_kw,priceData,timeDeltaseconds):
    """

    :param demand_kw: Demand in KW
    :param priceData: Array from API with each hour as an entry (should be 24 entries)
    :param priceDeltahour: diff in seconds from wo timeperiods
    :return: Price to pay
    """
    now = datetime.now()
    #print("now: " , now)
    #print(value['datetime'].hour)

    price = 0;

    for value in priceData:

        if(value['datetime'].hour == now.hour):

            price = value['value']/1000 # Price per MWh divided by 1000 for €/kwh
    return [price * demand_kw * timeDeltaseconds/3600, price]

#print(calCosts (8,pr,1000))