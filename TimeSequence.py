import datetime

t_start = datetime.datetime.now()

def hour3seq ():


    with open('UserTemperature.csv', 'w', newline='') as csvFile:
        # Create a CSV reader
        writer = csv.writer(csvFile)
        writer.writerow([min(self.sdiv.getValue(), 52)])
        csvFile.close()
    t_now = datetime.datetime.now()
    time_diff = (t_now - t_start).total_seconds()