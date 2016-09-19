#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See:
# - http://docs.scipy.org/doc/scipy/reference/optimize.html
# - http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
# - http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult
# - http://www.scipy-lectures.org/advanced/mathematical_optimization/
# - http://students.mimuw.edu.pl/~pbechler/scipy_doc/tutorial/optimize.html
# - https://people.duke.edu/~ccc14/sta-663/BlackBoxOptimization.html

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize


# DEFINE THE OBJECTIVE FUNCTION ###############################################

def f(x):
    #return np.sin(2. * 2. * np.pi * x) * 1. / np.sqrt(2. * np.pi) * np.exp(-(x**2.)/2.)
    return np.power(x, 2.)


# OPTIMIZE ####################################################################

x0 = 1.
result = optimize.minimize(f, x0)

# Global view of the result
print(result)

# See http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult
print("Does the optimizer exited successfully ?", result.success)
print("The solution of the optimization:", result.x)
print("Termination status of the optimizer:", result.status)
print("Values of objective function:", result.fun)
print("Number of evaluations of the objective function:", result.nfev)
print("Number of iterations performed by the optimizer:", result.nit)


# PLOT THE FUNCTION AND THE RESULT ############################################

# Build datas
x = np.arange(-5, 5, 0.01)
y = f(x)

# Plot data
fig = plt.figure(figsize=(8.0, 8.0))
ax = fig.add_subplot(111)

ax.plot(x, y, "-", label=r"Objective function $f$")
ax.plot(result.x, result.fun, "or", label=r"Optimum")

# Set title and labels
ax.set_title(r"Minimize", fontsize=20)
ax.set_xlabel(r"$x$", fontsize=32)
ax.set_ylabel(r"$f(x)$", fontsize=32)

# Set legend
ax.legend(loc='upper right', fontsize=20)

# Save file
plt.savefig("minimize_1d.png")

# Plot
plt.show()
