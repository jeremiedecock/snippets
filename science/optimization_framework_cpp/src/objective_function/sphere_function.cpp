/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include "sphere_function.h"
#include <cassert>

/**
 * 
 */
SphereFunction::SphereFunction(int _ndim) {
    this->ndim = _ndim;
    this->domainMin = std::vector<double>(this->ndim, -1.);
    this->domainMax = std::vector<double>(this->ndim,  1.);
}

/**
 * 
 */
double SphereFunction::operator() (const std::vector<double> & x) const {
    // Only one sample
    assert(x.size() == this->ndim);

    double y;

    for(int i=0 ; i<x.size() ; i++) {
        y += x[i] * x[i];
    }

    return y;
}
