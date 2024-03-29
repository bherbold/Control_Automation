# -*- coding: utf-8 -*-
"""
Created on Friday 6th January 2023

@authors: José Luz, Bendiks Herbold
"""
# importing libraries
import csv
import time

import datetime


def PID(arduino, max_on):
    try:
        print("enter PID")
        # SEND MESSAGE
        arduino.write('H'.encode())
        preSteam = 0
        preTemp = 0
        pre_water_temp = 0
        t_pre = datetime.datetime.now()

        T_set = 50
        K_p = 10 # P Gain
        #K_d = -5000 # D Gain f
        K_d = -700  # D Gain f

        time.sleep(1)

        with open('../Control_Automation/Data_Management/lastReading.csv', 'r') as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Iterate over the rows of the CSV
            for row in reader:
                # Get the value from the second column (index 1)
                preTemp = float(row[4])
                preSteam = float(row[6])
                onOff = float(row[1])
                pre_water_temp = float(row[7])

        while (True):
            time.sleep(1)
            # Open the CSV file
            with open('../Control_Automation/Data_Management/lastReading.csv', 'r') as file:
                # Create a CSV reader
                reader = csv.reader(file)

                # Iterate over the rows of the CSV
                for row in reader:
                    # Get the value from the second column (index 1)
                    sauna_temp = float(row[4])
                    steam = float(row[6])
                    onOff = float(row[1])
                    water_temp = float(row[7])

            with open('../Control_Automation/Data_Management/UserTemperature.csv', 'r') as file:
                # Create a CSV reader
                reader = csv.reader(file)

                for row in reader:
                    # Get the value from the second column (index 1)
                    T_set = float(row[0])

            if T_set == 48: # eco mode (48 is actually not the temperature-> It varies between 47 and 50)
                print("Eco Mode")

                if sauna_temp >= 50:
                    T_set = 47
                elif sauna_temp <= 47:
                    T_set = 50
            else:
                print("Regular Mode")

            # PID Start
            T_sauna_diff = T_set - sauna_temp
            t_now = datetime.datetime.now()
            time_diff = (t_now - t_pre).total_seconds()

            # D
            D = (sauna_temp - preTemp)/(time_diff)

            # Seconds on (PD addition)
            #on_time = min((T_sauna_diff * K_p)+(T_sauna_diff * D * K_d), max_on)  # limited to max_on seconds
            on_time = min((T_sauna_diff * K_p) + (D * K_d), max_on)  # limited to max_on seconds
            print("On Seconds: ", on_time)
            print("T_set: ", T_set)
            print("T_sauna: ", sauna_temp)
            print("Temp_diff: ", T_sauna_diff)
            print("Time_diff: ", time_diff)
            print("K_p * T_diff: ", (T_sauna_diff * K_p))
            print("D: ", D)
            #print("D * K_d * T_diff: ", (T_sauna_diff * D * K_d))
            print("D * K_d: ", (D * K_d))


            arduino.write('L'.encode())
            print('Plug ON (PID)')
            time.sleep(max(on_time, 0))
            arduino.write('H'.encode())
            print('Plug OFF (PID)')
            time.sleep(30) # settle time always 10 sec

            if water_temp <= 28:
                print("Leave PID to try Cold Start")
                print("Water Temp: ", water_temp, " °C")
                break

            # set pre-Values
            preSteam = steam
            preTemp = sauna_temp
            pre_water_temp = water_temp
            t_pre = t_now



    # handling KeyboardInterrupt by the end-user (CTRL+C)
    except KeyboardInterrupt:
        # closing communications port
        arduino.close()
        print('Communications closed')