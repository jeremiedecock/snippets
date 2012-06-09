/* 
 * UniformRandomNumberGenerator
 * Generate random real numbers (uniform distribution) using boost::random.
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.random library
 */

#include <ctime>

#include "random_number_generator.h"

/**
 * Constructor.
 */
UniformRandomNumberGenerator::UniformRandomNumberGenerator(double min, double max) : min(min), max(max) {
    // Pseudo-random number generator
    this->rng = new boost::mt19937(std::time(NULL));

    // Random number distribution (that maps to min..max)
    this->distrib = new boost::uniform_real<>(this->min, this->max);

    // Generator (wrapper)
    this->boostRandomGenerator = new boost::variate_generator< boost::mt19937&, boost::uniform_real<> >(*rng, *distrib);
}

/**
 * Destructor.
 */
UniformRandomNumberGenerator::~UniformRandomNumberGenerator() {
    delete this->boostRandomGenerator;
    delete this->distrib;
    delete this->rng;
}

/**
 * Return a random number (between this->min and this->max).
 */
double UniformRandomNumberGenerator::generateNumber() const {
    double x = (* this->boostRandomGenerator)();
    return x;
}

