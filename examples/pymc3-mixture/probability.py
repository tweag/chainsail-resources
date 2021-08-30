"""
Example probability density for consumption by Chainsail
"""
import numpy as np

import pymc3 as pm


class PyMC3GaussianMixture(object):
    def __init__(self, means, sigmas, weights):
        self.means = means
        self.sigmas = sigmas
        self.weights = weights

        def sigma_to_cov(sigma):
            return np.array([[1 / sigma ** 2, 0], [0, 1 / sigma ** 2]])

        with pm.Model() as model:
            components = [pm.MvNormal.dist(mu=mu, cov=sigma_to_cov(sigma))
                          for mu, sigma in zip(means, sigmas)]
            pm.Mixture("coords", w=weights, comp_dists=components, shape=(2,))

        self.model = model

    def log_prob(self, x):
        return self.model.logp(x)

    def log_prob_gradient(self, x):
        return self.model.dlogp_array(x)


means = np.array([[-1.0, -2.0], [1.0, 1.0], [3.0, 2.0], [2.0, -2.0]])
n_components = len(means)
sigmas = np.ones(n_components) / 3
weights = np.ones(n_components) / n_components
weights /= weights.sum()

pdf = PyMC3GaussianMixture(means, sigmas, weights)
initial_states = np.array([-1.0, 0.5])
