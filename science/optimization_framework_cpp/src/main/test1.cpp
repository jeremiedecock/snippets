/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include <iostream>
#include <cstdlib>

#include "sphere_function.h"
#include "optimizer_naive.h"
#include "optimizer_gradient_descent.h"

int main(int argc, char * argv[])
{
    srand(time(NULL)); // TODO
    srand48(time(NULL)); // TODO

    ObjectiveFunction * objective_function = new SphereFunction();
    //Optimizer * optimizer = new OptimizerNaive();
    Optimizer * optimizer = new OptimizerGradientDescent(0.001, 0.5);
    optimizer->minimize(*objective_function, 100);

    return 0;
}
