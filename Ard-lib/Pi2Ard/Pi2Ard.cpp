#include <Arduino.h>
#include "Pi2Ard.h"

Pi2Ard::Pi2Ard()
{
}

void Pi2Ard::connect(const int &baudRate)
{
    Serial.begin(baudRate);
}

void Pi2Ard::disconnect()
{
    Serial.end();
}

void Pi2Ard::send(const char *data)
{
    Serial.println(data);
}