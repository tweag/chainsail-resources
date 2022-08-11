"""
Probability density of a Gaussian mixture defined by a PyMC model
"""

import numpy as np
import pymc as pm

from chainsail_helpers.pdf.pymc import PyMCPDF


means = np.array([[-1.0, -2.0], [1.0, 1.0], [3.0, 2.0], [2.0, -2.0]])
n_components = len(means)
sigmas = np.ones(n_components) / 3
weights = np.ones(n_components) / n_components
weights /= weights.sum()


def sigma_to_cov(sigma):
    return np.array([[sigma ** 2, 0], [0, sigma ** 2]])


with pm.Model() as model:
    components = [pm.MvNormal.dist(mu=mu, cov=sigma_to_cov(sigma))
                  for mu, sigma in zip(means, sigmas)]
    pm.Mixture("coords", w=weights, comp_dists=components, shape=(2,))


pdf = PyMCPDF(model)
# This is the concatenation of the flattened
# values of all PyMC model variables in alphabetical order, so if
# you have two variables var1 and var2 with shapes (2, 2) and (3,),
# x is (in pseudo code) (x1, x2, x3, x4, x5, x6, x7) with
# (x1, ..., x4) = var1.flatten()
# and (x5, ..., x7) = var2.flatten().
initial_states = np.array([-1.0, 0.5])
