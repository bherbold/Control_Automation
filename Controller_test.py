# -*- coding: utf-8 -*-
"""
Created on Friday 6th January 2023

@authors: José Luz, Bendiks Herbold
"""
# importing libraries
import serial
import datetime as dt
import re
import csv
import time

import HelperFunc
import REE_API as RAPI

def relayControlTest(arduino):
    try:
        print("enter Controller")
        # SEND MESSAGE
        arduino.write('L'.encode())
        preSteam = 0
        preTemp = 0
        time.sleep(1)
        while(True):
            time.sleep(1)
            # Open the CSV file
            with open('lastReading.csv', 'r') as file:
                # Create a CSV reader
                reader = csv.reader(file)

                # Iterate over the rows of the CSV
                for row in reader:
                    # Get the value from the second column (index 1)
                    sauna_temp = row[4]
                    steam = row[6]
                    onOff = row[1]
                    water_temp = row[7]

            if float(sauna_temp) <= 45 and (float(onOff) == 0):

                preSteam = float(steam)
                arduino.write('H'.encode())
                print('Plug ON (auto)')
            if (float(steam)-float(preSteam) >= 3) or (float(water_temp) >= 47) and (float(onOff) == 1.0):

                arduino.write('L'.encode())
                time.sleep(20)
                print('Plug off (auto)')

            #print('Light on or off?')

            """reply = int(input('Light on or off? - 1 for on, 0 for off'))

            if (reply == 1):
                arduino.write('H'.encode())
                print('Plug ON')
            elif (reply == 0):
                arduino.write('L'.encode())
                print('Plug off')
            else:
                print('Try again')"""

    # handling KeyboardInterrupt by the end-user (CTRL+C)
    except KeyboardInterrupt:
        # closing communications port
        arduino.close()
        print('Communications closed')