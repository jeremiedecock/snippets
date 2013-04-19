#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np

import sys

sys.path.append("src")

import function
import optimizer

# MAIN ########################################################################

def main():

    #f = function.SphereFunction(2)
    #f = function.NoisedSphereFunction(2)
    #f = function.Sin1Function()
    #f = function.Sin2Function()
    #f = function.Sin3Function()
    f = function.YahooFunction()

    #opt = optimizer.NaiveMinimizer()
    #opt = optimizer.GradientDescent(delta=0.01)
    opt = optimizer.SaesHgb(x_init=np.ones(f.ndim))

    best_x = opt.optimize(f, num_gen=3000)
    #best_x = opt.optimize(f, num_samples=3000)

    print "Best sample: f(", best_x, ") = ", f(best_x)

if __name__ == '__main__':
    main()

