/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include "objective_function.h"
#include <cassert>

double ObjectiveFunction::operator() (const std::vector<double> & x) const {
    // Only one sample
    assert(x.size() == this->ndim);
    double y = this->eval_one_sample(x);

    return y;
}

std::vector<double> ObjectiveFunction::operator() (const std::vector<std::vector<double> > & x_vec) const {
    // Multiple samples
    std::vector<double> y_vec = this->eval_multiple_samples(x_vec);

    return y_vec;
}

std::vector<double> ObjectiveFunction::eval_multiple_samples(const std::vector<std::vector<double> > & x) const {
    std::vector<double> y_vec;

    for(int i=0 ; i<x.size() ; i++) {
        double y = this->eval_one_sample(x[i]);
        y_vec.push_back(y);
    }

    return y_vec;
}

void ObjectiveFunction::plot(const std::vector<double> & xmin, const std::vector<double> & xmax) const {
    // TODO
}

int ObjectiveFunction::getDimension() const {
    return this->ndim;
}

std::vector<double> ObjectiveFunction::getDomainMin() const { 
    return this->domainMin;
}

std::vector<double> ObjectiveFunction::getDomainMax() const {
    return this->domainMax;
}

