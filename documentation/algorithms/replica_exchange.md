# Replica Exchange: the main ingredient of Chainsail

Replica Exchange is the Markov Chain Monte Carlo (MCMC) algorithm at the heart of Chainsail and it's main feature. 
In a nutshell, Replica Exchange works by sampling a series of increasingly "flatter" versions (_replicas_) of a probability distribution with a "local" MCMC algorithm such as [Hamiltonian Monte Carlo](./hmc.md) and occasionally exchanging states between all those separate Markov chains.
That way, the Markov chain that samples the distribution of interest can escape from modes it is otherwise likely to be trapped in.  
Replica Exchange requires the choice of a series of probability distributions, which interpolate between the target distribution and some very easy to sample, "flat" distribution.
It is convenient to choose a parameterized family of "tempering" distributions and then vary its parameter to set a _schedule_.
While that family of tempering distributions is essentially arbitrary, Chainsail currently implements only the most traditional and popular one, where `p(x|beta)=p(x)^beta` with `0 < beta <= 1` and `p(x)` your probability distribution of interest. If your sampling problem requires are a different family of tempering distributions, please open an [issue](https://github.com/tweag/chainsail-resources/issues) to let us know and if it turns out that your tempering distribution family is requested by others, too, we might find the resources to implement it.  
If you'd like to learn more about Replica Exchange, check out Tweag's ([blog post](https://www.tweag.io/blog/2020-10-28-mcmc-intro-4/)) on the topic!

