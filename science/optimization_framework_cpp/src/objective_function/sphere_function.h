/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#ifndef SPHERE_FUNCTION_H
#define SPHERE_FUNCTION_H

#include "objective_function.h"

class SphereFunction : public ObjectiveFunction {

    public:

        SphereFunction(int _ndim=1);

    protected:

        double eval_one_sample(const std::vector<double> & x) const;

};

#endif //SPHERE_FUNCTION_H
