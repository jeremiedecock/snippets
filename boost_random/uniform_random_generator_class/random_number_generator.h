/* 
 * RandomNumberGenerator
 * Generate random real numbers (uniform distribution) using boost::random.
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.random library
 */

#ifndef RANDOM_NUMBER_GENERATOR_H
#define RANDOM_NUMBER_GENERATOR_H

#include <boost/random.hpp>
#include <boost/random/uniform_real.hpp>

class RandomNumberGenerator
{
    private:
        // Pseudo-random number generator
        boost::mt19937 * rng;

        // Random number distribution (that maps to min..max)
        boost::uniform_real<> * distrib;

        // Generator (wrapper)
        boost::variate_generator< boost::mt19937&, boost::uniform_real<> > * boostRandomGenerator;
        
    public:
        const double min;
        const double max;

    public:
        RandomNumberGenerator(double, double);
        ~RandomNumberGenerator();
        double generateNumber() const;
};

#endif // RANDOM_NUMBER_GENERATOR_H
