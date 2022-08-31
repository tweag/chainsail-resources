# Replica Exchange: the main ingredient of Chainsail

## General idea
Replica Exchange is the Markov Chain Monte Carlo (MCMC) algorithm at the heart of Chainsail and its main feature. 
In a nutshell, Replica Exchange works by sampling a series of increasingly "flatter" versions (_replicas_) of a probability distribution with a "local" MCMC algorithm such as [Hamiltonian Monte Carlo](./hmc.md) and occasionally exchanging states between all those separate Markov chains.
That way, the Markov chain that samples the distribution of interest can escape from modes it is otherwise likely to be trapped in.  

## Tempered ("flattened") distributions
Replica Exchange requires the choice of a series of probability distributions, which interpolate between the target ("cold") distribution and some very easy to sample, "flat" ("hot") distribution.
It is convenient to choose a parameterized family of "tempering" distributions and then vary its parameter to set a _schedule_.
While that family of tempering distributions is essentially arbitrary, Chainsail currently implements two tempering schemes.

### Global tempering
The most traditional and popular one tempering scheme is one where 

$$
p(x|\beta)=p(x)^\beta
$$

with $0 < \beta \leq 1$ and $p(x)$ your probability distribution of interest.
$\beta$ is often referred to as an (inverse) temperature in analogy to the [canonical ensemble](https://en.wikipedia.org/wiki/Canonical_ensemble) in statistical physics.

### Likelihood tempering
In Bayesian inference, we have $p(x|D) \propto p(D|x) \times p(x)$.
$p(x|D)$ is the posterior distribution and usually what a Chainsail user wants to sample.
It is proportional to the product of the likelihood $p(D|x)$ and the prior $p(x)$.
Often, the prior is not very hard to sample, so a sensible choice for a tempering scheme is to apply an inverse temperature $\beta$ only to the likelihood, like so:

$$ p(x|D, \beta) \propto p(D|x)^\beta \times p(x) $$

For $\beta=1$, we sample from the full posterior, while for $0 < \beta \ll 1$ the likelihood and thus the influence of the data are essentially switched off.

## Choice of inverse temperatures
If, for two neighboring (in the schedule sense) replicas, the values for $\beta$ are too different, exchanges between those replicas are unlikely to be accepted.
If, on the other hand, all replicas are very close in $\beta$ space, many exchanges will be accepted, but also many, many replicas are required to bridge between the target (cold) replica and the flattest (hottest) copy, potentially wasting computing resources.

To find the sweet spot, Chainsail implements an iterative [schedule tuning](./schedule_tuning.md) algorithm.  
If your sampling problem requires are a different family of tempering distributions, please open an [issue](https://github.com/tweag/chainsail-resources/issues) to let us know and if it turns out that your tempering distribution family is requested by others, too, we might find the resources to implement it.  

## Further reading
If you'd like to learn more about Replica Exchange, check out Tweag's ([blog post](https://www.tweag.io/blog/2020-10-28-mcmc-intro-4/)) on the topic!

