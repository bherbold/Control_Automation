from Controller import Controller_main as CON_main
from Data_Management import Data_Management as DM, HelperFunc
import serial

arduino = serial.Serial(str(HelperFunc.get_ESP32_port()), 115200, timeout=3)


# Python3 program to write file in
# background

def Main():


    background = DM.AsyncWrite(arduino)
    background.start()

    #UserInput = UI.AsyncWrite()
    #UserInput.start()
    #CON.relayControl(arduino)
    #CON_test.relayControlTest(arduino)
    CON_main.Controller_main(arduino)
    # wait till the background thread is done
    background.join()
    print("Waited until thread was complete")

if __name__ == '__main__':
    Main()