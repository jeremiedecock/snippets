#!/usr/bin/env python

"""
This is a simple Octave implementation of the (mu/mu_I, lambda)-sigmaSA-ES
as discussed in 
http://www.scholarpedia.org/article/Evolution_Strategies
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import random


MU = 3                    # number of parents
LAMBDA = 12               # number of offspring

X_INIT = np.ones(1)       # initial parent vector 
#X_INIT = np.ones(2)       # initial parent vector 
SIGMA_INIT = 1            # initial global mutation strength sigma 

SIGMA_MIN = 1e-10         # ES stops when sigma is smaller than sigma_min

###########################################################

# Function to be optimized (sphere test function as an example)
# individual: the individual to evaluate
def sphere_function(indiv):
    x = indiv.x
    assert x.shape == X_INIT.shape, x
    y = np.dot(x, x)
    return y

def sin1(indiv):
    x = indiv.x
    assert x.shape == (1,), x
    x = np.absolute(x)
    y = np.sin(2 * 2 * np.pi * x) * np.exp(-5 * x)
    return y

def sin2(indiv):
    x = indiv.x
    assert x.shape == (1,), x
    y = np.sin(2 * 2 * np.pi * x) * 1/np.sqrt(2*np.pi) * np.exp(-(x**2)/2)
    return y

from matplotlib.finance import quotes_historical_yahoo
import datetime

date1 = datetime.date( 1995, 1, 1 ) 
date2 = datetime.date( 2004, 4, 12 )
quotes = quotes_historical_yahoo('INTC', date1, date2)
yahoo_data = [-q[1] for q in quotes]

def yahoo(indiv):
    x = indiv.x
    assert x.shape == (1,), x

    y = 0
    if 0 <= x < len(yahoo_data):
        y = yahoo_data[int(x)]
    return y

#fitness = sphere_function
#fitness = sin1
#fitness = sin2
fitness = yahoo

###########################################################

# The individual class
# x: the individual's value
# sigma: the individual's sigma
class Individual():
    def __init__(self, x, sigma):
        self.x = x
        self.sigma = sigma
        self.cost = fitness(self)
    # TODO: redef print

###########################################################

# This sorts the population according to the individuals' fitnesses
# pop: a list of Individual objects
def select_individuals(pop):
    pop.sort(key=lambda indiv: indiv.cost, reverse=False)
    return pop[:MU]

# This performs intermediate (multi-) recombination
# parents: a list of Individual objects
def recombine_individuals(parents):
    parents_y = np.array([indiv.x for indiv in parents])
    parents_sigma = np.array([indiv.sigma for indiv in parents])
    recombinant = Individual(parents_y.mean(axis=0), parents_sigma.mean())
    return recombinant

###########################################################

def main():

    # Initialization
    n = X_INIT.shape[0]         # determine search space dimensionality n   
    tau = 1. / math.sqrt(2.*n)  # self-adaptation learning rate

    # Initializing individual population
    parent_pop = [Individual(X_INIT, SIGMA_INIT) for i in range(MU)]

    # Evolution loop of the (mu/mu_I, lambda)-sigma-SA-ES
    while parent_pop[0].sigma > SIGMA_MIN:
        offspring_pop = []
        recombinant = recombine_individuals(parent_pop)
        for i in range(1, LAMBDA):
            offspring_sigma = recombinant.sigma * math.exp(tau * random.normalvariate(0,1))
            offspring_y = recombinant.x + offspring_sigma * np.random.normal(size=n)
            offspring = Individual(offspring_y, offspring_sigma)
            offspring_pop.append(offspring)
        parent_pop = select_individuals(offspring_pop)
        print parent_pop[0].x, parent_pop[0].sigma, parent_pop[0].cost

# Remark: Final approximation of the optimizer is in "parent_pop[0].x"
#         corresponding fitness is in "parent_pop[0].cost" and the final 
#         mutation strength is in "parent_pop[0].sigma"

if __name__ == "__main__":
    main()
