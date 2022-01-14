import numpy as np
import matplotlib.pyplot as plt

samples = np.load("sc_samples.npy")

data = np.loadtxt("data.txt").T

fig, ax = plt.subplots()
ax.scatter(*data.T, label="data")
colors = ("green", "red", "blue", "black", "yellow", "gray", "orange", "lightblue", "cyan")
for s in samples[1000::100]:
    s = s.reshape(-1, 2)
    for i, c in enumerate(s):
        ax.scatter((c[0],), (c[1],), color=colors[i], s=75, marker="x", alpha=0.5)
ax.legend()
plt.show()
