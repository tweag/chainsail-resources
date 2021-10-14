# Replica Exchange: the main ingredient of Chainsail

TODO

Chainsail is essentially a Replica Exchange ([blog post](https://www.tweag.io/blog/2020-10-28-mcmc-intro-4/)) implementation with automated temperature schedule tuning deployed on a cloud computing platforms to provide the necessary parallel computing power.

In a nutshell, Replica Exchange is a Markov chain Monte Carlo (MCMC) algorithm that works by simulating a series of increasingly "flatter" versions (_replicas_) of a probability distribution with a "local" MCMC algorithm such as Hamiltonian Monte Carlo ([blog post](https://www.tweag.io/blog/2020-08-06-mcmc-intro3/)) and occasionally exchanging states between all those simulations.
That way, the Markov chain that samples the distribution of interest can escape from modes it is otherwise likely to be trapped in. 
Replica Exchange requires the choice of a series of probability distributions, which interpolate between the target distribution and some very easy to sample, "flat" distribution.
It is convenient to choose a parameterized family of "tempering" distributions and then vary its parameter to set a _schedule_.
The only family of distributions currently implemented is of the form `p(x|beta)=p(x)^beta` with `0 < beta <= 1` and `p(x)` your probability distribution of interest.
