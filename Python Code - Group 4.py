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

# creating communications object using Serial 
arduino = serial.Serial('/dev/cu.usbserial-14110', 115200, timeout=3)
print("Starting!")

# try-except-finally loop for data acquisition
try:
    while True:
        now = dt.datetime.now() 
        # SEND MESSAGE
        
        print('Light on or off?\n')
        
        reply = int(input('Light on or off? - 1 for on, 0 for off \n'))
        
        if (reply == 1):
            arduino.write('H'.encode())
            print ('Plug ON')
        elif (reply == 0):
            arduino.write('L'.encode())
            print ('Plug OFF')
        else:
            print ('Try again')
            
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
            [v1, v2] = re.findall(pattern=r"[-+]?\d*\.\d+|[-+]?\d+", string=data)  # to understand pattern: https://regex101.com/
            # store date and readings (change them to float!) into a list
            row = [now, float(v1),float(v2)]
            # save reading row into the csv file. File needs to be open with "a" (append) mode.
            with open('Test_Control.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                csvFile.close()
                print(row)
        else:
            print('No data is being collected')
              
# handling KeyboardInterrupt by the end-user (CTRL+C)
except KeyboardInterrupt:
    # closing communications port
    arduino.close() 
    print('Communications closed')
    