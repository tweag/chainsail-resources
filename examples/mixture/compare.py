import argparse
import numpy as np
import matplotlib.pyplot as plt

from plots import plot_true_distribution, plot_samples_histogram

parser = argparse.ArgumentParser(
    description="Compare single chain and Chainsail sampling results for a 2D mixture model"
)
parser.add_argument("--sc_samples", type=str, default="sc_samples.npy", help="Results of single chain sampling (via single_chain.py)")
parser.add_argument(
    "--chainsail_samples",
    type=str,
    default="chainsail_samples.npy",
    help='Results of chainsail sampling (via ../../postprocessing/concatenate_samples.py)',
)
args = parser.parse_args()

sc_samples = np.load(args.sc_samples)
re_samples = np.load(args.chainsail_samples)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
plot_true_distribution(ax1)
plot_samples_histogram(ax2, sc_samples, "single chain")
plot_samples_histogram(ax3, re_samples, "RE via Chainsail")
plt.show()
