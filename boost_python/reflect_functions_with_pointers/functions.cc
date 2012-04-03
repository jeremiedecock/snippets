#include "functions.h"

// Pointers ///////////////////////////////////////////////////////////////////

void pointer_wrong(double * x) {
    (*x)++;
}

void pointer_right(MuttableNumber * x) {
    x->value += 1;
}

