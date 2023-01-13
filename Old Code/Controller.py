# -*- coding: utf-8 -*-
"""
Created on Friday 6th January 2023

@authors: José Luz, Bendiks Herbold
"""
# importing libraries

def relayControl(arduino):
    try:
        print("enerter Controller")
        # SEND MESSAGE
        arduino.write('L'.encode())
        while(True):
            print('Light on or off?')

            reply = int(input('Light on or off? - 1 for on, 0 for off'))

            if (reply == 1):
                arduino.write('H'.encode())
                print('Plug ON')
            elif (reply == 0):
                arduino.write('L'.encode())
                print('Plug off')
            else:
                print('Try again')

    # handling KeyboardInterrupt by the end-user (CTRL+C)
    except KeyboardInterrupt:
        # closing communications port
        arduino.close()
        print('Communications closed')