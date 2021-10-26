# Chainsail resources and documentation
Examples, documentation and other additional resources related to the Chainsail sampling web service (https://chainsail.io).

## Chainsail: a web service to sample multimodal probability distributions
Chainsail is a web service which helps you sample from multimodal probability distributions.
In the context of Bayesian statistics, they arise in the case of unidentifiable parameters which are due to some symmetry in the model or if you have ambiguous data.  
While this early version of Chainsail is targeted towards experienced Markov Chain Monte Carlo (MCMC) practitioners, it is still designed to be user-friendly and in this repository, we provide some documentation on how to use Chainsail and the algorithms at work behind the scene.

## Usage
Learn how to use Chainsail in only 13 steps :-)
Don't worry, it's not as complicated as it sounds.
Check out the walkthrough [here](./documentation/walkthrough.md).
If you have any questions, don't hesitate to [shoot us a message](mailto:support@chainsail.io)!

## The algorithms behind Chainsail
Chainsail implements several important algorithms, which we describe here in not too much detail:
- [Replica Exchange](./documentation/algorithms/replica_exchange.md): Chainsail's main ingredient that allows you to sample multimodal probability distributions
- [Automatic Replica Exchange tuning](./documentation/algorithms/schedule_tuning.md): Replica Exchange requires setting a kind of "temperature" schedule, which Chainsail automatically determines for you
- [Hamiltonian Monte Carlo](./documentation/algorithms/hmc.md): While Replica Exchange takes care of _global_ sampling, meaning it helps to discover all modes of your probability distribution, _local_ sampling algorithms like Hamiltonian Monte Carlo sample well within a single mode. Chainsail currently only implements a very simple form of Hamiltonian Monte Carlo.

## The `chainsail_helpers` package
This repository also contains the source code for the [`chainsail_helpers`](./chainsail_helpers/) package.
It defines the interface for Chainsail-compatible probability distributions, PPL-specific implementations of them and provides helper scripts.


## Questions?
Shoot us an [email](mailto:support@chainsail.io)!
