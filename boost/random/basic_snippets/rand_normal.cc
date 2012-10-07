/* 
 * Rand_normal: generate random numbers (normal distribution) using boost::random.
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.random library
 * Usage: g++ rand_normal.cc
 *
 */

#include <boost/random.hpp>
#include <boost/random/normal_distribution.hpp>
#include <ctime>
#include <iostream>

const int num_it = 100000;
const double min = 1.0;
const double max = 10.0;
const double mu = 0.0;
const double sigma = 1.0;

main() {

    // Pseudo-random number generator
    //boost::mt19937 rng;               // deterministic
    boost::mt19937 rng(std::time(NULL));

    // Random number distribution
    boost::normal_distribution<> distrib(mu, sigma);

    // Generator (wrapper)
    boost::variate_generator<boost::mt19937&, boost::normal_distribution<> > random_generator(rng, distrib);

    for(int i=0 ; i<num_it ; i++) {
        double x = random_generator();
        double y = random_generator();
        std::cout << x << " " << y << std::endl;
    }

}
