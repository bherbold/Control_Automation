# import requests library
import requests
import json
# import plotting library
#import matplotlib
#import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

def get_real_price_now ():
    # datetime object containing current date and time
    now = datetime.now()
    # Time formate for REE API
    dt_string_start = now.strftime("%Y/%m/%dT%H:00")
    #print("date and time =", dt_string)

    endpoint = 'https://apidatos.ree.es'
    get_archives = '/en/datos/mercados/precios-mercados-tiempo-real'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Host': 'apidatos.ree.es'}
    #params = {'start_date': 'dt_string', 'end_date': '2019-10-16T23:00', 'time_trunc': 'hour'}
    params = {'start_date': dt_string_start, 'time_trunc': 'hour'}

    response = requests.get(endpoint + get_archives, headers=headers, params=params)



    print(response)






