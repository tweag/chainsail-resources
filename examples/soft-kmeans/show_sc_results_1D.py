from probability import pdf
import numpy as np
import matplotlib.pyplot as plt
import sys

samples = np.load(sys.argv[1])
data = np.loadtxt(sys.argv[2]).T[:, None]

if len(samples.shape) == 3:
    samples = samples[:,0]
print(samples.shape)

# data = np.loadtxt("data_1D_overlapping.txt").T[:, None]

print("Average negative log-probability:",
      np.mean([-pdf.log_prob(x) for x in samples]))

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.hist(data.squeeze().ravel(), bins=20, histtype="step", label="data", density=True)
ax1.hist(samples[:,0], bins=70, alpha=0.5, density=True, label="$\mu_1$")
ax1.hist(samples[:,1], bins=70, alpha=0.5, density=True, label="$\mu_2$")
ax1.legend()

space = np.linspace(-2, 6, 200)
vals = [np.exp(pdf.log_prob(np.array([x, y]))) for y in space for x in space]
ax2.pcolor(space, space, np.array(vals).reshape(200, 200))
ax2.plot(*samples[::100].squeeze().T, color="white", alpha=0.2, label="MCMC trace")
ax2.set_xlabel("$\mu_1$")
ax2.set_ylabel("$\mu_2$")
ax2.legend()

ax3.hist(samples[:,0], bins=70, density=True)
ax3.set_xlim((-2, 6))
ax3.set_xlabel("$\mu_1$")
ax4.hist(samples[:,1], bins=70, density=True)
ax4.set_xlim((-2, 6))
ax4.set_xlabel("$\mu_2$")

for ax in (ax1, ax3, ax4):
    for spine in ("top", "left", "right"):
        ax.spines[spine].set_visible(False)
    ax.set_yticks(())

fig.tight_layout()
plt.show()

