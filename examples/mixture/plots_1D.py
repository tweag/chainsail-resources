import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import quad

from probability import GaussianMixture

np.seterr(all='raise')


def flatten_samples(f):
    def wrapped_func(*args, **kwargs):
        samples = [x[0] for x in args[0]]
        new_args = [arg for arg in args]
        new_args[0] = samples
        return f(*new_args, **kwargs)

    return wrapped_func


def make_axes(sample_space_lim, fig):
    traceax = plt.subplot2grid(shape=(1, 5), loc=(0, 0), colspan=4, fig=fig)
    distax = plt.subplot2grid(shape=(1, 5), loc=(0, 4), fig=fig)
    traceax.set_yticks(())
    distax.set_xlim(sample_space_lim)
    traceax.set_ylim(sample_space_lim)
    distax.set_xticks(())
    for spine in ['top', 'bottom', 'right']:
        distax.spines[spine].set_visible(False)
    for spine in ['top', 'right', 'left']:
        traceax.spines[spine].set_visible(False)
    traceax.set_xlabel("# of MCMC samples")

    return distax, traceax


def plot_pdf(pdf, distax, int_lims=(-5, 5)):
    Z = quad(lambda x: np.exp(pdf.log_prob(x)), *int_lims)[0]
    xspace = np.linspace(*distax.get_xlim(), 200)
    probs = [np.exp(pdf.log_prob(x)) / Z for x in xspace]
    distax.plot(probs, xspace)
    distax.set_xlim((0, max(probs) * 1.2))


@flatten_samples
def plot_hist(samples, distax, bins=30):
    distax.hist(samples, bins=bins, density=True, orientation='horizontal')


@flatten_samples
def plot_trace(samples, traceax, step=5):
    traceax.plot(np.arange(len(samples))[::step], samples[::step], ls='-', alpha=0.3, marker='.')


def main():
    parser = argparse.ArgumentParser(
        description="Plot MCMC samples of 1D Gaussian mixture"
    )
    parser.add_argument(
        "--samples-file",
        type=str,
        help='Path to .npy file with samples to plot',
        required=False
    )
    args = parser.parse_args()


    pdf = GaussianMixture(np.array([0]), np.array([1]), np.array([1]))
    pdf = GaussianMixture(np.array([[-2], [2]]), np.array([0.3, 0.5]), np.array([1, 0.6]))

    if args.samples_file:
        samples = np.load(args.samples_file)
    else:
        # draw samples using (single-chain) Metropolis algorithm
        sys.path.append('../')
        from rwmc import RWMCSampler

        sampler = RWMCSampler(pdf, np.array([1.0]), 1.2)
        samples = [sampler.sample() for _ in range(5000)]
        print("Acceptance rate: {:.2f}".format(sampler.acceptance_rate))

    fig = plt.figure(figsize=(12, 3))
    sample_space_lim = (-4, 4)
    distax, traceax = make_axes(sample_space_lim, fig)
    plot_pdf(pdf, distax)
    plot_hist(samples, distax, bins=50)
    plot_trace(samples, traceax, step=5)
    fig.tight_layout()
    
    plt.show()


if __name__ == '__main__':
    main()
