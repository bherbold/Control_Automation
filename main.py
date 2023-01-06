import Controller as CON
import Data_Management as DM
import threading

if __name__ == "__main__":
    # Create the threads
    thread1 = threading.Thread(target=CON.relayControl())
    thread2 = threading.Thread(target=DM.dataManagement())

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()

    print("All threads done!")