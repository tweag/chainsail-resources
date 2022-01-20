"""
Hacky script to concatenate target replica samples
"""
import argparse
import os

import numpy as np


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate batches of MCMC samples into a single .npy file"
    )
    parser.add_argument(
        "simulation_run",
        type=str,
        help='Simulation run, e.g. "/some/path/to/production_run"'
    )
    parser.add_argument("output_file", type=str, help="Output file")
    args = parser.parse_args()

    with open(os.path.join(args.simulation_run, "config.yml")) as f:
        dump_interval = None
        for l in f.readlines():
            if l.lstrip().startswith("dump_interval"):
                dump_interval = int(l.split(":")[1].strip())

    ctr = 0
    samples = []
    while True:
        try:
            fname = "samples_replica1_{}-{}.pickle".format(
                ctr, ctr + dump_interval)
            samples += np.load(os.path.join(args.simulation_run,
                               "samples", fname), allow_pickle=True)
            ctr += dump_interval
        except FileNotFoundError:
            break

    np.save(args.output_file, np.array(samples))


if __name__ == '__main__':
    main()
