# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 13:54:24 2019

@authors: Ingrid, Cristian, Marc - CITCEA
"""
# importing libraries
import serial
import datetime as dt
import re
import csv

import HelperFunc
import REE_API as RAPI

# creating communications object using Serial
#arduino = serial.Serial('/dev/cu.usbserial-14330', 115200, timeout=3)
arduino = serial.Serial(str(HelperFunc.get_ESP32_port()), 115200, timeout=3)

print("Starting!")

preTime = dt.datetime.now()
priceList = RAPI.get_real_price_day() # store values from Price API

# try-except-finally loop for data acquisition
try:

    # SEND MESSAGE

    print('Light on or off?')

    reply = 3 #int(input('Light on or off? - 1 for on, 0 for off'))

    if (reply == 1):
        arduino.write('H'.encode())
        print('Plug ON')
    elif (reply == 0):
        arduino.write('L'.encode())
        print('Plug off')
    else:
        print('Try again')

    row = ["TimeStamp", "Power_W", "Current", "Sauna Temperature", "Humidity", "Steam", "Water Temperature", "Cost", "Price_EUR_kWh"]
    with open('2hourTest.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
        csvFile.close()

    while True:
        now = dt.datetime.now()
        timeDiff = ((now - preTime).total_seconds()) # needed for Cost calculation

        #Update Price array when new day starts
        if now.hour == 0:
            priceList = RAPI.get_real_price_day()

        # SEND MESSAGE

        # READ DATA
        # Check if there is new info from the Arduino and read it
        print("start read")
        data_bytes = arduino.readline()
        print(
            data_bytes
        )
        print("finish read")
        # Decoding the message into UTF-8
        data = data_bytes.decode("utf-8")

        # SAVE DATA
        # if data has been read, print and save it
        if data:
            # strip data string into 2, 3 or as many different values for each reading
            [power, current, sauna_temp, sauna_humidity, steam, water_temp] = re.findall(pattern=r"[-+]?\d*\.\d+|[-+]?\d+",
                                  string=data)  # to understand pattern: https://regex101.com/
            # store date and readings (change them to float!) into a list
            row = [now, float(power), float(current), float(sauna_temp), float(sauna_humidity), float(steam), float(water_temp),
                   float(RAPI.calCosts(float(power)/1000,priceList,timeDiff)[0]), float(RAPI.calCosts(float(power)/1000,priceList,timeDiff)[1])]
            # save reading row into the csv file. File needs to be open with "a" (append) mode.
            with open('2hourTest.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                csvFile.close()
                #print(row)
        else:
            print('No data is being collected')

        preTime = now
# handling KeyboardInterrupt by the end-user (CTRL+C)
except KeyboardInterrupt:
    # closing communications port
    arduino.close()
    print('Communications closed')
