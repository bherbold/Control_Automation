import streamlit as st
from collections import namedtuple
import math
import pandas as pd
import numpy as np
import plost                # this package is used to create plots/charts within streamlit
from PIL import Image       # this package is used to put images within streamlit

# import requests library
import requests
import json

#from api_connection import get_data_from_api       # keep this commented if not using it otherwise brakes the app

url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q":"Barcelona","days":"1"}

headers = {
	"X-RapidAPI-Key": "6648a2da2cmshf825bca858b5edep1244d2jsna590481eee52",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response = response.json()
Demand_High = False # will the demand for the steam sauna high today?

temp_opening_hours = []
sum_Temp_opening_hours = 0
opening_hour = 6
closing_hour = 22

for i in range((opening_hour-1),(closing_hour-1)):
    temp_hour =  response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    sum_Temp_opening_hours = sum_Temp_opening_hours + temp_hour
    temp_opening_hours.append(temp_hour)
ave_Temp_opening_hours = sum_Temp_opening_hours/(closing_hour-opening_hour)

Demand_High = ave_Temp_opening_hours <14

# Page setting
st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Data
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')
# replace the previous data with your own streamed data from API

### Here starts the web app design
# Row A
a1, a2, a3 = st.columns(3)
a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
a2.metric("Wind", "9 mph", "-8%")
a3.metric("Humidity", "86%", "4%")

# Row B
b1, b2, b3, b4 = st.columns(4)
b1.metric("Temperature - Barcelona", str(int(ave_Temp_opening_hours)), "1")
b2.metric("Wind", "9 mph", "-8%")
b3.metric("Humidity", "86%", "4%")
b4.metric("Humidity", "86%", "4%")

# Row C
c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### TEST')              # text is created with markdown
    plost.time_hist(                        # histogram
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color='temp_max',
    aggregate='median',
    legend=None)
with c2:
    st.markdown('### Bar chart')
    plost.donut_chart(                      # donut charts
        data=stocks,
        theta='q2',
        color='company')
