/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#ifndef OPTIMIZER_GRADIENT_DESCENT_H
#define OPTIMIZER_GRADIENT_DESCENT_H

#include "optimizer.h"

class OptimizerGradientDescent : public Optimizer
{
    protected:
        double precision;
        double stepSize;

    public:
        OptimizerGradientDescent(double _precision = 0.0001, double _step_size = 0.01);

        std::vector<double> minimize(const ObjectiveFunction & objective_function, int num_samples=1000);
};

#endif  // OPTIMIZER_GRADIENT_DESCENT_H
