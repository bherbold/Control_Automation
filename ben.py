import streamlit as st
import bookingManager as BM
import streamlit_authenticator as stauth
import REE_API as API_data
from collections import namedtuple
import datetime
import math
import pandas as pd
import numpy as np
import plost                # this package is used to create plots/charts within streamlit
from PIL import Image

def update_bookings ():
    schedule = BM.loads_matrix()
    mode_array = []

    for hour in schedule:
        if hour['mode'] == 'Regular':
            mode_array.append('Regular')
        elif hour['mode'] == 'Economic':
            mode_array.append('Eco')
        else:
            mode_array.append('No Booking')
        
    #print(mode_array)