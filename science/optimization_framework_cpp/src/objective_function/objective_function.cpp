/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include "objective_function.h"

std::vector<double> ObjectiveFunction::operator() (const std::vector<std::vector<double> > & x_vec) const {
    // Multiple samples
    std::vector<double> y_vec;

    for(int i=0 ; i<x_vec.size() ; i++) {
        double y = this->operator()(x_vec[i]); // call itself (functor)
        y_vec.push_back(y);
    }

    return y_vec;
}

void ObjectiveFunction::plot(const std::vector<double> & xmin, const std::vector<double> & xmax) const {
    // TODO
}

/////////

int ObjectiveFunction::getDimension() const {
    return this->ndim;
}

std::vector<double> ObjectiveFunction::getDomainMin() const { 
    return this->domainMin;
}

std::vector<double> ObjectiveFunction::getDomainMax() const {
    return this->domainMax;
}

