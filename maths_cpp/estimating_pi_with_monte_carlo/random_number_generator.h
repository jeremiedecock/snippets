/* 
 * UniformRandomNumberGenerator
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

class UniformRandomNumberGenerator
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
        UniformRandomNumberGenerator(double, double);
        ~UniformRandomNumberGenerator();
        double generateNumber() const;
};

#endif // RANDOM_NUMBER_GENERATOR_H
