/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include "optimizer_gradient_descent.h"
#include "tools/utils.h"

#include <algorithm>
#include <vector>
#include <cstdlib>
#include <ctime>

OptimizerGradientDescent::OptimizerGradientDescent(double _precision, double _step_size) {
    this->precision = _precision;
    this->stepSize = _step_size;
}

std::vector<double> OptimizerGradientDescent::minimize(const ObjectiveFunction & objective_function, int num_samples)
{
    assert(num_samples > 0);

    std::vector<double> x;
    for(int i=0 ; i<objective_function.getDimension() ; i++) {
        x.push_back(drand48() * 20. - 10.);            // TODO: use std::random
    }

    std::vector<double> gradient(objective_function.getDimension(), 0.);

    PRINT(this->precision);
    PRINT(this->stepSize);

    for(int cpt_gen = 0 ; cpt_gen < num_samples ; cpt_gen++) {

        PRINT_VEC(x);

        // GRADIENT ///////////////////////////////////////
        
        for(int index_dim=0 ; index_dim<objective_function.getDimension() ; index_dim++) {        // foreach dim
            // Sample 1
            std::vector<double> x1 = x;
            x1[index_dim] += this->precision;
            const double y1 = objective_function(x1);
        
            // Sample 2
            std::vector<double> x2 = x;
            x2[index_dim] -= this->precision;
            const double y2 = objective_function(x2);
        
            // GRADIENT
            gradient[index_dim] = y1 - y2;
        }
        
        PRINT_VEC(gradient);
       
        for(int i=0 ; i<objective_function.getDimension() ; ++i) {
            x[i] = x[i] - this->stepSize * gradient[i]; // minimization
            //x[i] = x[i] + this->stepSize * gradient[i]; // maximization
        }

        const double y = objective_function(x);
        PRINT(y);
    }

    return x;
}
