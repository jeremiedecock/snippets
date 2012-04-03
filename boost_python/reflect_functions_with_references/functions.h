#ifndef functions_h
#define functions_h

#include <iostream>

// MuttableNumbers

class MuttableNumber {
    public:
    double value;
};

// References

void reference_wrong(double &);

void reference_right(MuttableNumber &);

#endif // functions_h
