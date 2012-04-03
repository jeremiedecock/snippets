#include "functions.h"

void reference_wrong(double & x) {
    x++;
}

void reference_right(MuttableNumber & x) {
    x.value += 1;
}

