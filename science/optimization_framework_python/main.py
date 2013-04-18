#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np

import sys

sys.path.append("src")

#import function.noised_sphere as function
#import function.sphere as function
#import function.sin1 as function
#import function.sin2 as function
import function.sin3 as function
#import function.yahoo as function

import optimizer.naive as optimizer
#import optimizer.gradient as optimizer

# MAIN ########################################################################

def main():

    #f = function.SphereFunction(2)
    #f = function.NoisedSphereFunction(2)
    #f = function.Sin1Function()
    #f = function.Sin2Function()
    f = function.Sin3Function()
    #f = function.YahooFunction()

    opt = optimizer.NaiveMinimizer()
    #opt = optimizer.GradientDescent(delta=0.01)

    best_x = opt.optimize(f, num_samples=1000)

    print "Best sample: f(", best_x, ") = ", f(best_x)

if __name__ == '__main__':
    main()

