import os
import numpy as np
from scipy.special import logsumexp, softmax

from chainsail_helpers.pdf import PosteriorPDF

# `data` is of dimensions (n_points, n_dim)
path = os.path.dirname(os.path.abspath(__file__))
data = np.loadtxt(os.path.join(path, "data.txt"), ndmin=2)


class Pdf(PosteriorPDF):
    def __init__(
        self,
        prior_sigma,
        prior_mean,
        weights,
        data,
        likelihood_sigma=1,
    ):
        self.prior_sigma = prior_sigma
        self.prior_mean = prior_mean
        self.weights = np.array(weights) / np.array(weights).sum()
        self.data = data
        self.likelihood_sigma = likelihood_sigma
        self.n_dim = data.shape[1]
        self.n_clusters = len(self.weights)

    def log_prior(self, x):
        x = x.reshape(self.n_clusters, self.n_dim)
        return -0.5 * np.sum((x - self.prior_mean) ** 2, 1).sum() \
            / self.prior_sigma ** 2

    def log_prior_gradient(self, x):
        x = x.reshape(self.n_clusters, self.n_dim)
        gradient = -(x - self.prior_mean) / self.prior_sigma ** 2
        return gradient.ravel()

    def log_likelihood(self, x):
        # Reshape x & data to dimensions (n_clusters, n_dim, n_data_points)
        x = x.reshape(self.n_clusters, self.n_dim)[:, :, np.newaxis]
        data = self.data.T[np.newaxis, :, :]
        log_likelihood_per_datum = logsumexp(
            -0.5 * np.sum((x - data) ** 2, 1)
            + np.log(self.weights[:, np.newaxis])
            / (self.likelihood_sigma ** 2), 0)
        return log_likelihood_per_datum.sum()

    def log_likelihood_gradient(self, x):
        # Reshape x & data to dimensions (n_clusters, n_dim, n_data_points)
        x = x.reshape(self.n_clusters, self.n_dim)[:, :, np.newaxis]
        data = self.data.T[np.newaxis, :, :]
        d_outer = softmax(
            -0.5 * np.sum((x - data) ** 2, 2)
            / (self.likelihood_sigma ** 2)
            + np.log(self.weights)[:, np.newaxis])
        grad_per_cluster_and_datum = -(x - data) * d_outer[:, :, np.newaxis]
        return grad_per_cluster_and_datum.sum(axis=2).ravel()


pdf = Pdf(
    prior_sigma=5,
    prior_mean=np.array([[1], [1]]),
    weights=[80, 120],
    data=data,
)
initial_states = np.array([1., 0.])


# 2D example

# pdf = Pdf(
#     prior_sigma=5,
#     prior_mean=np.array([[0, 0], [0, 0]]),
#     weights=[80, 160],
#     data=data,
# )
# initial_states = np.array([[0, 1], [0, 1]]).ravel()
