# Pi2Ard

## Introduction
This is an archive of a project I did. The task was to transfer temperature data from a PT100 sensor to an Arduino and then onto a Raspberry Pi. Feel free to use any of the code in any way.

## Software dependencies
* [Adafruit_MAX31865][1]
* [Kivy][2]
* [Kivy Garden][3]
* [Graph in Kivy Garden][4] (install with `garden install graph`)
* [pySerial][5]

## Installing this code
1. Get the dependencies
2. Add the Arduino Pi2Ard library to the Arduino IDE by going `Sketch > Include Library > Add .ZIP Library...` and point it to _Ard-lib/Pi2Ard_.
3. Open Pi2Ard.ino in the Arduino IDE and download it to the Arduino.
3. Stick the _Pi-lib/Pi2Ard_ folder anywhere on your Raspberry Pi.
4. Connect the two together with the Arduino's USB cable
5. Run _Pi-lib/gui/main.py_ with a Python 3 interpreter

## Technical details
Please see the [wiki][6] for more details on the design and implementation of this code

[1]: https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/arduino-code
[2]: https://kivy.org/
[3]: https://kivy-garden.github.io/
[4]: https://github.com/kivy-garden/garden.graph
[5]: https://pyserial.readthedocs.io/
[6]: https://github.com/Red-Leader117/Pi2Ard/wiki
