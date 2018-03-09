#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot a loglog histogram of a large input data (larger than memory) with generator

Fill the histogram chunk by chunk.
Use a generator to get samples (to make an easily reusable snippet).

See:
- https://stackoverflow.com/questions/33371917/how-to-plot-result-of-np-histogram-with-matplotlib-analog-to-plt-his
- https://stackoverflow.com/questions/5328556/histogram-matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

def sample_generator(max_num_samples, chunk_size=100):

    mu, sigma = 1000, 1000

    cpt = 0
    while cpt <= max_num_samples:
        samples = np.random.normal(loc=mu, scale=sigma, size=chunk_size)
        cpt += chunk_size
        yield samples


def make_hist(it, vmin, vmax, nbins):
    """Make an histogram of large data (chunk by chunk).
    
    Parameters
    ----------
    it : iterable object
        An iterable object that provides samples.
    vmin : float
        The first bin.
    vmax : float
        The last bin.
    nbins : int
        The number of bins.
    """
    
    bins = np.logspace(vmin, vmax, nbins)
    hist, bins = np.histogram([], bins=bins)
        
    # ITERATE OVER IMAGES #########################################

    for samples in it:        
        hist += np.histogram(samples, bins=bins)[0]
        
    return hist, bins


def plot_hist(hist, bins, title):
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.step(bins[:-1], hist, linewidth=1.5, where='post',
            label=r'X = $\mathcal{N}(1000, 1000)$')

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_title(title, fontsize=20)
    ax.set_xlabel("X", fontsize=32)
    ax.set_ylabel("Counts", fontsize=32)

    ax.legend(loc='best', fontsize=16)

    return ax


it = sample_generator( max_num_samples=1000000)
hist, bins = make_hist(it, vmin=-1., vmax=4., nbins=250)
ax = plot_hist(hist, bins,
               title="Big data histogram ({} samples)".format(sum(hist)))

# Save file ###########################

plt.savefig("hist_big_data_log_log_with_generic_generator.png")

# Plot ################################

plt.show()
