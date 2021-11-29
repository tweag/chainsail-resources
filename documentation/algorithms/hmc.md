# Hamiltonian Monte Carlo in Chainsail

Hamiltionian Monte Carlo (HMC) is a popular Markov Chain Monte Carlo (MCMC) algoritm.
While MCMC algorithms in general allow (at least, in theory) sampling of arbitrary probability distributions, HMC samples continous probability distributions (densities) very efficiently by exploiting the local geometry of the probability.
See, for example, Tweag's [HMC blog post](https://www.tweag.io/blog/2020-08-06-mcmc-intro3/) for a thorough introduction to HMC's inner workings.

## Limitations of the HMC implementation
Currently, Chainsail is in beta stage and the development effort has been on the [Replica Exchange](./replica_exchange.md) part, which enhances _global_ sampling and is Chainsail
s main feature.
For that reason, Chainsail currently implements only a very simple version of HMC which does the _local_ sampling.
HMC has a range of important parameters that need to be tuned carefully for it to work optimally.
There is only a basic automatic adaption of the integration step size, a unit mass matrix and a fixed number of integration steps per HMC step. 
The HMC implementation will be improved or replaced with an existing state-of-the-art implementation in later stages of the project.
If you feel that the HMC implementation provided is what prevents Chainsail from being useful for you, let us know in a [GitHub issue](https://github.com/tweag/chainsail-resources/issues).
