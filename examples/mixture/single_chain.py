import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from probability import pdf, initial_states
from plots import plot_true_distribution, plot_samples_histogram

this_dir = os.path.dirname( __file__ )
up_dir = os.path.abspath(os.path.join(this_dir, '..'))
sys.path.append(up_dir)
from rwmc import RWMCSampler

sampler = RWMCSampler(pdf, initial_states, 0.5)

samples = []
n_samples = 10000
for i in range(n_samples):
    samples.append(sampler.sample())

    if i % 500 == 0 and i > 1:
        print("Samples: {}/{} ### acceptance rate: {:.2f}".format(
            i, n_samples, sampler.acceptance_rate))

fig, (ax1, ax2) = plt.subplots(1, 2)
plot_true_distribution(ax1)
plot_samples_histogram(ax2, np.array(samples), "single chain")
fig.tight_layout()
plt.show()

np.save(os.path.join(this_dir, "sc_samples.npy"), np.array(samples))
