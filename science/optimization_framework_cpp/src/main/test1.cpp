/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include <iostream>
#include <cstdlib>

#include "sphere_function.h"
#include "optimizer_naive.h"

int main(int argc, char * argv[])
{
    srand(time(NULL)); // TODO

    ObjectiveFunction * objective_function = new SphereFunction();
    Optimizer * optimizer = new OptimizerNaive();
    optimizer->minimize(*objective_function, 10);

    return 0;
}
