/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include "optimizer_naive.h"
#include "tools/utils.h"
#include "tools/random_number_generator.h"

#include <algorithm>
#include <vector>
#include <cstdlib>
#include <ctime>

std::vector<double> OptimizerNaive::minimize(const ObjectiveFunction & objective_function, int num_samples)
{
    assert(num_samples > 0);

    std::vector<std::vector<double> > x_samples;
    std::vector<double> y_samples;

    // Generate num_samples random points
    for(int i=0 ; i<num_samples ; i++) {
        x_samples.push_back(this->generateRandomPoint(objective_function));
    }

    PRINT_VEC_VEC(x_samples);

    // Evaluate previously generated points
    y_samples = objective_function(x_samples);
    //for(int i=0 ; i<num_samples ; i++) {
    //    std::vector<double> x = x_samples[i];
    //    double y = objective_function(x);
    //    y_samples.push_back(y);
    //}

    PRINT_VEC(y_samples);
    
    // Find the minimum
    int index_min = 0;
    for(int i=0 ; i<num_samples ; i++) {
        if(y_samples[i] < y_samples[index_min]) {
            index_min = i;
        }
    }

    std::vector<double> x_min = x_samples[index_min];

    PRINT_VEC(x_samples[index_min]);
    PRINT(y_samples[index_min]);

    return x_min;
}

std::vector<double> OptimizerNaive::generateRandomPoint(const ObjectiveFunction & objective_function) const
{
    static RandomNumberGenerator random_generator(0., 1.);

    std::vector<double> dmin = objective_function.getDomainMin();
    std::vector<double> dmax = objective_function.getDomainMax();
    int x_dim = objective_function.getDimension();

    std::vector<double> x;
    for(int i=0 ; i<x_dim ; i++) {
        x.push_back(random_generator.generateNumber() * (dmax[i] - dmin[i]) + dmin[i]); // TODO denormalize in dmin dmax
    }
    
    return x;
}

