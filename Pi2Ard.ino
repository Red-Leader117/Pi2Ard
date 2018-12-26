#include <Adafruit_MAX31865.h>
#include <Pi2Ard.h>

const float RREF        = 430.0;
const float RNOMINAL    = 100.0;
const int   delaySec    = 1;
const int   SIZE        = 20;

Adafruit_MAX31865 sensor = Adafruit_MAX31865(10, 11, 12, 13);

Pi2Ard link = Pi2Ard();

char sendText[SIZE];

void setup() {
  sensor.begin(MAX31865_2WIRE);
  link.connect(9600);
}

void loop() {
  // Check and print any faults
  uint8_t fault = sensor.readFault();
  if (fault) {
    // Ignore fault
    dtostrf(0.0, 4, 2, sendText);
    link.send(sendText);
    sensor.clearFault();
  }
  else
  {
    dtostrf(sensor.temperature(RNOMINAL, RREF), 5, 2, sendText);
    link.send(sendText);
  }
  delay(delaySec * 1000);
}
