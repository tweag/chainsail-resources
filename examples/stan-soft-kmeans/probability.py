"""
Probability density of a Gaussian mixture defined by a Stan model
"""

import numpy as np

from chainsail_helpers.pdf.stan import StanPDF
import json


data_points = np.loadtxt("data.txt").T.tolist()
nb_dimensions = 2
nb_clusters = 9
data = {
  "N": len(data_points),
  "D": nb_dimensions,
  "K": nb_clusters,
  "y": data_points,
}

model_code = """
data {
  int<lower=0> N;  // number of data points
  int<lower=1> D;  // number of dimensions
  int<lower=1> K;  // number of clusters
  vector[D] y[N];  // observations
}
transformed data {
  real<upper=0> neg_log_K;
  neg_log_K = -log(K);
}
parameters {
  vector[D] mu[K]; // cluster means
}
transformed parameters {
  real<upper=0> soft_z[N, K]; // log unnormalized clusters
  for (n in 1:N)
    for (k in 1:K)
      soft_z[n, k] = neg_log_K - 0.5 * dot_self(mu[k] - y[n]);
}
model {
  // prior
  for (k in 1:K)
    mu[k] ~ std_normal();

  // likelihood
  for (n in 1:N)
    target += log_sum_exp(soft_z[n]);
}
"""

pdf = StanPDF(model_code, data=data)
initial_states = np.random.uniform(0, 6, size=nb_dimensions*nb_clusters)
