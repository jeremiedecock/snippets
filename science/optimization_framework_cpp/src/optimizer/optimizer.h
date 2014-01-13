/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#ifndef OPTIMIZER_H
#define OPTIMIZER_H

#include "objective_function.h"
#include <vector>

class Optimizer
{
    public:
        virtual std::vector<double> minimize(const ObjectiveFunction & objective_function, int num_samples) = 0;
};

#endif  // OPTIMIZER_H
