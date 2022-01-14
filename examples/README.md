# Example Chainsail use cases
This provides several simple use cases for Chainsail, in which a single Markov chain fails to accurately sample a multimodal distribution. Each use case consists of several files, the most important of which are:
- a `probability.py`, in which the PDF to be sampled as well as an initial state is specified and which can be consumed by Chainsail,
- a script `single_chain.py` which samples from the PDF using a single Markov chain constructed by a very simple Metropolis algorithm and shows the result,
- a script `compare.py` which compares the results of single-chain sampling and results obtain by Replica Exchange via Chainsail,
- and potentially a script `make_data.py`, which creates a data set from which parameters of a Bayesian model in `probability.py` are inferred.

The typical workflow to try out these use cases would be
1. Run `python single_chain.py` in one of the example case directories (writes samples to a file `sc_samples.npy`, possibly install the dependencies in `requirements.txt`) and be unhappy with the result,
2. run Chainsail using the same `probability.py`, but zipped and uploaded to some URL,
3. download the Chainsail results, unzip them and concatenate them to a single `numpy` array written to the example case directory by running (in this directory)
   ```bash
   $ unzip /path/to/results.zip -d /some/path
   $ concatenate-samples /some/path/simulation_run /some/path/chainsain_samples.npy
   ```
   `concatenate-samples` is a Python script available in the `chainsail-helpers` package.
4. Run `python compare.py <example dir>/sc_samples.npy /some/path/chainsail_samples.npy` in the use case directory and (ideally) be amazed how much better Chainsail sampled your distribution :-)
