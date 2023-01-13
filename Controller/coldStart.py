import time
import datetime
import csv

def coldStart (arduino, startTemp, startupTime):

    print("COLD START")
    t_start = datetime.datetime.now()
    t_now = datetime.datetime
    time_diff = 0
    water_temp = 0
    steam_diff = 0
    time.sleep(1)
    started = False

    # Open the CSV file
    with open('../Control_Automation/Data_Management/lastReading.csv', 'r') as file:
        # Create a CSV reader
        reader = csv.reader(file)
        # Iterate over the rows of the CSV
        for row in reader:
            # Get the value from the second column (index 1)
            steam_start = float(row[6])



    while (time_diff <= startupTime and float(water_temp) <= startTemp and steam_diff <= 1):



        # Open the CSV file
        with open('../Control_Automation/Data_Management/lastReading.csv', 'r') as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Iterate over the rows of the CSV
            for row in reader:
                # Get the value from the second column (index 1)
                sauna_temp = row[4]
                steam = row[6]
                onOff = row[1]
                water_temp = row[7]
        steam_diff = float(steam) - steam_start
        t_now = datetime.datetime.now()
        time_diff = (t_now - t_start).total_seconds()
        arduino.write('L'.encode())
        if started == False:
            print('Plug ON (StartUp)')
            started = True


