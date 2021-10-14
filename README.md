# Chainsail resources and documentation
Examples, documentation and other additional resources related to Chainsail

## Chainsail: a web service to sample multimodal probability distributions
Chainsail is a web service which helps you sample from multimodal probability distributions. In the context of Bayesian statistics, they arise in the case of unidentifiable parameters which are due to some symmetry in the model or if you have ambiguous data.

## Usage
Learn how to use Chainsail in only 13 steps :-)
Don't worry, it's not as complicated as it sounds.
Check out the walkthrough [here](./documentation/walkthrough.md).
If you have any questions, don't hesitate to [shoot us a message](mailto:support@chainsail.io)!

## The algorithms behind Chainsail
Without spilling too many beans of this currently closed-source project, [here](./documentation/algorithms/README.md) is some background information for if you're interested what algorithms power Chainsail.
Chainsail implements
- [Replica Exchange](./documentation/algorithms/replica_exchange.md) to facilitate multimodal sampling,
- [automated Replica Exchange schedule adaption](./documentation/algorithms/schedule_tuning.md) based on work by Prof. Michael Habeck (see these [two](http://proceedings.mlr.press/v22/habeck12.html) [papers](https://arxiv.org/abs/1504.00053)),
- and a currently very simple version of [Hamiltonian Monte Carlo (HMC)](./documentation/algorithms/hmc.md).

## The `chainsail_helpers` package
This repository also contains the source code for the `chainsail_helpers` package.
It defines the interface for Chainsail-compatible probability distributions, PPL-specific implementations of them and helper scripts.


## Questions?
Shoot us an [email](mailto:support@chainsail.io)!
