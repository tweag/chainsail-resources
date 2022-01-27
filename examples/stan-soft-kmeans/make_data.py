import sys
import numpy as np

# Parameters
means = [(0, 0), (0, 3), (3, 0), (9, 6)]
covs = [
    np.array([[0.5, 0], [0, 0.4]]),
    np.array([[0.5, 0], [0, 0.3]]),
    np.array([[0.3, 0], [0, 0.3]]),
    np.array([[0.1, 0], [0, 0.1]])
]
sizes = [200, 250, 150, 50]
np.random.seed(0)

# Data generation
data_points = []
for (mean_x, mean_y), cov, size in zip(means, covs, sizes):
    mean_x += np.random.uniform(-0.5, 0.5)
    mean_y += np.random.uniform(-0.5, 0.5)
    data_points.append(
        np.random.multivariate_normal((mean_x, mean_y), cov, size=np.random.choice(np.arange(int(size*0.9), int(size*1.1)))))
data_points = np.vstack(data_points)
print(data_points.shape)

# Plot data points
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(*data_points.T, alpha=0.5)
plt.show()

# Save to file
np.savetxt(sys.argv[1], data_points.T)
