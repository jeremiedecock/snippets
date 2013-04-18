# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

__all__ = ['SaesHgb', 'Individual']

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import random

import optimizer

"""
The individual class
- x: the individual's value
- sigma: the individual's sigma
"""
class Individual():
    def __init__(self, x, sigma, y):
        self.x = x
        self.sigma = sigma
        self.y = y           # cost or reward

    def __str__(self):
        return "{0} {1} {2}".format(self.x, self.sigma, self.y)

"""
SAES
http://www.scholarpedia.org/article/Evolution_strategies
https://homepages.fhv.at/hgb/downloads/mu_mu_I_lambda-ES.oct
"""
class SaesHgb(optimizer.Optimizer):

    def __init__(self, mu=3, lambda_=12, x_init=None, sigma_init=1, sigma_min=1e-5):
        self.mu = mu                    # number of parents
        self.lambda_ = lambda_          # number of offspring
        self.x_init = x_init            # initial parent vector 
        self.sigma_init = sigma_init    # initial global mutation strength sigma 
        self.sigma_min = sigma_min      # ES stops when sigma is smaller than sigma_min

        self.x_samples = []
        self.y_samples = []

    """
    This sorts the population according to the individuals' fitnesses
    - pop: a list of Individual objects
    """
    def select_individuals(self, pop):
        pop.sort(key=lambda indiv: indiv.y, reverse=False)
        return pop[:self.mu]

    """
    This performs intermediate (multi-) recombination
    - parents: a list of Individual objects
    """
    def recombine_individuals(self, parents):
        parents_y = np.array([indiv.x for indiv in parents])
        parents_sigma = np.array([indiv.sigma for indiv in parents])
        recombinant = Individual(parents_y.mean(axis=0), parents_sigma.mean(), 0) # TODO
        return recombinant

    def optimize(self, objective_function, num_gen=50):

        #if self.x_init is None:
        #    self.x_init = np.random.random(objective_function.ndim)
        #    self.x_init -= (objective_function.domain_min + objective_function.domain_max) / 2.  # TODO
        #    self.x_init *= (objective_function.domain_max - objective_function.domain_min)       # TODO
        #else:
        assert self.x_init.ndim == 1
        assert self.x_init.shape[0] == objective_function.ndim

        # Initialization
        n = self.x_init.shape[0]         # determine search space dimensionality n   
        tau = 1. / math.sqrt(2.*n)       # self-adaptation learning rate

        # Initializing individual population
        y = objective_function(self.x_init)
        parent_pop = [Individual(self.x_init, self.sigma_init, y) for i in range(self.mu)]

        gen_index = 0

        # Evolution loop of the (mu/mu_I, lambda)-sigma-SA-ES
        while parent_pop[0].sigma > self.sigma_min and gen_index < num_gen:
            offspring_pop = []
            recombinant = self.recombine_individuals(parent_pop)
            for i in range(1, self.lambda_):
                offspring_sigma = recombinant.sigma * math.exp(tau * random.normalvariate(0,1))
                offspring_x = recombinant.x + offspring_sigma * np.random.normal(size=n)
                offspring = Individual(offspring_x, offspring_sigma, objective_function(offspring_x))
                offspring_pop.append(offspring)
            parent_pop = self.select_individuals(offspring_pop)
            #parent_pop = self.select_individuals(parent_pop + offspring_pop)

            gen_index += 1

            self.x_samples.append(parent_pop[0].x)  # TODO use a "log" object instead
            self.y_samples.append(parent_pop[0].y)  # TODO
            print parent_pop[0]

        self.plotSamples(np.array(self.x_samples), np.array(self.y_samples).reshape([-1,1]))
        self.plotCosts(np.array(self.y_samples).reshape([-1,1]))

        return parent_pop[0].x

# Remark: Final approximation of the optimizer is in "parent_pop[0].x"
#         corresponding fitness is in "parent_pop[0].y" and the final 
#         mutation strength is in "parent_pop[0].sigma"
