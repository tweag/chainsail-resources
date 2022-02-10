import sys

import numpy as np

spacing = 1.5
sigma = 1.0
sl = 2

n_data_points = np.array([75, 100])
data_points = []
for i, mean_x in enumerate(np.arange(0, spacing * sl, spacing)):
    data_points += list(np.random.normal(mean_x, sigma, size=n_data_points[i]))
data_points = np.array(data_points).squeeze()
print(data_points)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.hist(data_points, bins=20, histtype="stepfilled", alpha=0.5)
plt.show()

np.savetxt(sys.argv[1], np.array(data_points)[None,:].T)
