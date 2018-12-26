__all__ = ["link"]
from pi2ard.link import Link

'''def openGui():
    #from pi2ard.gui.main import Pi2ArdApp
    #Pi2ArdApp().run()
    from time import time
    from serial import SerialException

    def onReceive(data):
        data = data.decode('utf-8').rstrip()
        print(data.split(','))

    t_end = time() + 20
    link = Link()
    print(link.checkAvailable())
    link.setOnReceive(onReceive)

    if link.checkAvailable() == True:
        link.connect()
        while time() < t_end:
            link.receive()

if __name__ == "__main__":
    openGui()'''