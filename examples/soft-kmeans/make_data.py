import sys

import numpy as np

spacing = 2.0
sigma = 0.5
sl = 2
n_dim = 2

cov = np.eye(n_dim) * sigma * sigma
n_data = 200
data_points = []
n_data_points = np.array([50, 150, 150, 50]).reshape(2,2)
# n_data_points = np.random.choice(np.arange(50,300), size=(sl, sl))
print(n_data_points)
for i, mean_x in enumerate(np.arange(0, spacing * sl, spacing)):
    for j, mean_y in enumerate(np.arange(0, spacing * sl, spacing)):
        mean_x += np.random.uniform(-0.5, 0.5)
        mean_y += np.random.uniform(-0.5, 0.5)
        data_points.append(
            np.random.multivariate_normal((mean_x, mean_y), cov, size=n_data_points[i, j]))
data_points = np.vstack(data_points)
print(data_points.shape)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(*data_points.T, alpha=0.5)
plt.show()

np.savetxt(sys.argv[1], data_points.T)
