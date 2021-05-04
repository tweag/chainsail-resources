# Example Chainsail use cases
This provides several simple use cases for RESAAS, in which a single Markov chain fails to accurately sample a multimodal distribution. Each use case consists of several files, the most important of which are:
- a `probability.py`, in which the PDF to be sampled as well as an initial state is specified and which can be consumed by Chainsail,
- a script `single_chain.py` which samples from the PDF using a single Markov chain constructed by a very simple Metropolis algorithm and shows the result,
- a script `compare.py` which compares the results of single-chain sampling and results obtain by Replica Exchange via Chainsail,
- and potentially a script `make_data.py`, which creates a data set, from which parameters of a Bayesian model are inferred.

The typical workflow to try out these use cases would be
1. run `python single_chain.py` in one of the example case directories (possibly install the dependencies in `requirements.txt`) and be unhappy with the result,
2. run Chainsail using the same `probability.py`, but zipped and uploaded to some URL
3. download the Chainsail results, unzip them and concatenate them to a single `numpy` array written to the example case directory by running (in this directory)
   ```bash
   $ cd ../../postprocessing
   $ unzip /path/to/results.zip
   $ python concatenate_samples.py --out ../examples/<example case directory>/chainsain_samples.npy
   ```
4. run `python compare.py` in the use case directory and (ideally) be amazed how much better Chainsail sampled your distribution :-)
