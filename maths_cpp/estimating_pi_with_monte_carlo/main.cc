/* 
 * Estimate Pi
 * Estimate Pi value using Monte Carlo method.
 *
 * Copyright (c) 2012 Jérémie Decock
 */

#include <iostream>
#include <cmath>

#include "random_number_generator.h"

const unsigned long num_random_points = 1000000;

int main() {
    double min = 0.0;
    double max = 1.0;

    UniformRandomNumberGenerator rng(min, max);

    unsigned long inside_circle = 0;

    std::cout << "Generating " << num_random_points << " random points..." << std::endl;

    for(unsigned long i=0 ; i<num_random_points ; i++) {
        double x = rng.generateNumber();
        double y = rng.generateNumber();

        if(pow(x, 2) + pow(y, 2) <= 1.0) {
            inside_circle++;
        }
    }

    /*
     * Compute pi (with r=1):
     *     area_square = r²
     *     area_circle = pi * r²
     *
     *     area_quarter_circle = pi * r² / 4
     * <=> area_quarter_circle = pi * area_square / 4
     * <=> pi = area_quarter_circle / area_square * 4
     *
     * Monte carlo:
     *     pi ~ num_random_points_inside_quarter_circle / num_random_points_iside_square * 4
     *     pi ~ inside_circle / num_random_points * 4
     */
    double pi = (double) inside_circle / (double) num_random_points * 4.0;

    std::cout.precision(9);
    std::cout << std::fixed << "Pi ~ " << pi << std::endl;

    return 0;
}
