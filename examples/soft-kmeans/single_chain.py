import numpy as np

import matplotlib.pyplot as plt

import sys
sys.path.append("../")
from rwmc import RWMCSampler

from probability import pdf, initial_state
from plots import plot_data_samples

sampler = RWMCSampler(pdf, initial_state, 0.05)
n = pdf.num_clusters


samples = []
accepted = 0
n_samples = 10000
for i in range(n_samples):
    samples.append(sampler.sample().reshape(-1, 2))
    
    if i % 500 == 0 and i > 1:
        print("Samples: {}/{} ### acceptance rate: {:.2f}".format(
            i, n_samples, sampler.acceptance_rate))
samples = np.array(samples)

fig, ax = plt.subplots()
plot_data_samples(ax, samples, "single chain")

np.save("sc_samples.npy", samples)
