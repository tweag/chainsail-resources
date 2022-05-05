import os
import numpy as np
from scipy.special import logsumexp, softmax


# `data` is of dimensions (n_points, n_dim)
path = os.path.dirname(os.path.abspath(__file__))
data = np.loadtxt(os.path.join(path, "data.txt"), ndmin=2)


class Pdf:
    def __init__(
        self,
        prior_sigma,
        prior_mean,
        weights,
        data,
        likelihood_sigma = 1,
    ):
        self.prior_sigma = prior_sigma
        self.prior_mean = prior_mean
        self.weights = np.array(weights)/np.array(weights).sum()
        self.data = data
        self.likelihood_sigma = likelihood_sigma
        self.n_dim = data.shape[1]

    def log_prior(self, x):
        # x is a sample, or a point in the space of the posterior,
        # which is of dimension n_clusters*n_dim
        # Reshape x to dimensions (n_clusters, n_dim)
        x = x.reshape(-1, self.n_dim)
        return -0.5 * np.sum((x - self.prior_mean) ** 2, 1).sum() \
            / self.prior_sigma ** 2

    def log_prior_gradient(self, x):
        # Reshape x to dimensions (n_clusters, n_dim)
        x = x.reshape(-1, self.n_dim)
        bla = -(x - self.prior_mean) / self.prior_sigma ** 2
        return bla.ravel()

    def log_likelihood(self, x):
        # Reshape x & data to dimensions (n_clusters, n_dim, n_data_points)
        x = x.reshape(-1, self.n_dim)[:,:,np.newaxis] 
        data = self.data.T[np.newaxis,:,:]
        a = logsumexp(
            -0.5 * np.sum((x - data) ** 2, 1) 
            + np.log(self.weights[:,np.newaxis])
            / (self.likelihood_sigma ** 2)
        , 0)
        return a.sum()

    def log_likelihood_gradient(self, x):
        # Reshape x & data to dimensions (n_clusters, n_dim, n_data_points)
        x = x.reshape(-1, self.n_dim)[:,:,np.newaxis]
        data = self.data.T[np.newaxis,:,:]
        d_outer = softmax(
            -0.5 * np.sum((x - data) ** 2, 2)
            / (self.likelihood_sigma ** 2) 
            + np.log(self.weights)[:,np.newaxis])
        im = -(x - data) * d_outer[:,:,np.newaxis]
        return im.sum(axis=2).ravel()

    def log_prob(self, x):
        return self.log_likelihood(x) + self.log_prior(x)

    def log_prob_gradient(self, x):
        return self.log_prior_gradient(x) + self.log_likelihood_gradient(x)

# n_dim = 1
pdf = Pdf(
    prior_sigma=5,
    prior_mean=np.array([[1], [1]]),
    weights=[80, 120],
    data=data,
)
initial_states = np.array([1., 0.])

# # n_dim = 2
# pdf = Pdf(
#     prior_sigma=5,
#     prior_mean=np.array([[0, 0], [0, 0]]),
#     weights=[80, 160],
#     data=data,
# )
# initial_states = np.array([[0, 1], [0, 1]]).ravel()
