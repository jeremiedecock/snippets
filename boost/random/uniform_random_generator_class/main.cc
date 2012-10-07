/* 
 * RandomNumberGenerator
 * Generate random real numbers (uniform distribution) using boost::random.
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.random library
 */

#include <iostream>

#include "random_number_generator.h"

int main() {
    double min = 0.0;
    double max = 1.0;

    RandomNumberGenerator rng(min, max);

    for(int i=0 ; i<10 ; i++) {
        std::cout << rng.generateNumber() << std::endl;
    }

    return 0;
}
