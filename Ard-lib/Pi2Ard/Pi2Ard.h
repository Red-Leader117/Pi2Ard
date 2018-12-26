#ifndef P2A_H
#define P2A_H

class Pi2Ard
{
public:
    Pi2Ard();

    void connect(const int &baudRate);

    void disconnect();

    void send(const char *data);
};

#endif
