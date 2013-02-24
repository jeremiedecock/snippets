#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import objective_functions
import optimizers

# MAIN ########################################################################

def main():

    #f = objective_functions.SphereFunction(2)
    f = objective_functions.NoisedSphereFunction(2)
    #f = objective_functions.TestFunction1()

    #opt = optimizers.NaiveMinimizer()
    opt = optimizers.GradientDescent(delta=0.01)

    best_x = opt.optimize(f, num_samples=1000)

    print "Best sample: f(", best_x, ") = ", f(best_x)

if __name__ == '__main__':
    main()

