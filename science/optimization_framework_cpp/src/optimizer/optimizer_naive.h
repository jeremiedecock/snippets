/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#ifndef OPTIMIZER_NAIVE_H
#define OPTIMIZER_NAIVE_H

#include "optimizer.h"

class OptimizerNaive : public Optimizer
{
    public:
        std::vector<double> minimize(const ObjectiveFunction & objective_function, int num_samples=1000);

    protected:
        std::vector<double> generateRandomPoint(const ObjectiveFunction & objective_function) const;
};

#endif  // OPTIMIZER_NAIVE_H
