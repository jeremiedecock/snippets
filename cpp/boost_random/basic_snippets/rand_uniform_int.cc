/* 
 * Rand_uniform_int: generate random integer numbers (uniform distribution) using boost::random.
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.random library
 * Usage: g++ rand_uniform_int.cc
 *
 */

#include <boost/random.hpp>
#include <boost/random/uniform_int.hpp>
#include <ctime>
#include <iostream>

const int num_it = 10;
const double min = 1.0;
const double max = 10.0;

main() {

    // Pseudo-random number generator
    //boost::mt19937 rng;
    boost::mt19937 rng(std::time(NULL));

    // Random number distribution (that maps to min..max)
    boost::uniform_int<> distrib(min, max);

    // Generator (wrapper)
    boost::variate_generator<boost::mt19937&, boost::uniform_int<> > random_generator(rng, distrib);

    for(int i=0 ; i<num_it ; i++) {
        //double x = distrib(rng);
        double x = random_generator();
        std::cout << x << " ";
    }

    std::cout << std::endl;

}
