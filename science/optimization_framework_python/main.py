#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np
import objective_functions
import optimizers

# MAIN ########################################################################

def main():

    f = objective_functions.SphereFunction(2)
    opt = optimizers.NaiveMinimizer()

    best_x = opt.optimize(f, num_samples=3)

    print "Best sample: f(", best_x, ") = ", f(best_x.reshape([1,-1]))

if __name__ == '__main__':
    main()

