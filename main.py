import traceback
from Processes.IOSApplicationResigner import IOSApplicationResigner

if __name__ == '__main__':
    try:
        App = IOSApplicationResigner()
        App.initialize()
        App.run()
    except Exception as e:
        print("Fatal Error has occurred exiting program.")
        traceback.print_exc()
