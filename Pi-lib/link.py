from platform import system
from serial import Serial, SerialException
from serial.tools.list_ports import comports

class Link:
    def __init__(self, port = None):
        self.serial = Serial(port)
        self.lastReceived = ''
        self.onReceive = None

    def setOnReceive(self, func):
        self.onReceive = func

    def isOpen(self):
        return self.serial.is_open

    def checkAvailable(self, port = None):
        port = self._getPort(port)
        list = comports()
        if len(list) == 0:
            return False
        else:
            for x in list:
                if x.device == port:
                    return True
        return False

    def connect(self, baudRate = None, port = None):
        if baudRate is None:
            self.serial.baudrate = 9600
        else:
            self.serial.baudrate = int(baudRate)

        try:
            self.serial.port = self._getPort(port)
        except SerialException as e:
            raise e
        else:
            self.serial.open()
            self.serial.reset_input_buffer()

    def clearBuffer(self):
            self.serial.reset_input_buffer()

    def disconnect(self):
        self.serial.close()

    def receive(self):
        if self.serial.in_waiting > 0:
            self.lastReceived = self.serial.readline()
            self.onReceive(self.lastReceived)

    def _getPort(self, port = None):
        sys = system()

        if sys == 'Windows':
            port = "COM3"
        elif sys == 'Linux':
            port = "/dev/ttyACM0"
        #elif port is None:
        #    raise SerialException("Error! Port was not given and could not be determined automatically.")

        return port
