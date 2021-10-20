# Automatic schedule adaption

A crucial setting of the [Replica Exchange](./replica_exchange.md) algorithm at the heart of Chainsail are the parameters of the interpolating distributions, which we call the _temperature schedule_. If these parameters are chosen incorrectly, Replica Exchange will either have troubles to correctly sample your probability distribution or waste a lot of computational resources.   
For this reason, Chainsail implements an iterative algorithm that automagically finds appropriate temperature schedules. It works by estimating the acceptance rate between two replicas as a function of their (inverse) temperaturs from previous, approximate samples of the probability distribution. The temperatures are then adapted such that the predicted acceptance rates between neighboring distributions attains a user-defined, constant value.  
Currently, only a single family of tempered probability distributions is implemented and for that family.
The schedule tuning algorithm then has three parameters which you can choose freely:
- the target acceptance rate (a value of 0.2 is likely a good choice),
- the minimum inverse temperature: the lower this value, the flatter the flattest probability distribution. You can start with a value of 0.1 and try a value of 0.01, if Chainsail doesn't sample your probability distribution correctly in spite of acceptance rates close to the above setting,
- the number of schedule optimization simulations: Chainsail performs a series of preliminary simulations to iteratively estimate a new schedule, sample from distributions following that schedule, and using those samples to obtain a more accurate estimation of the desired schedule with constant acceptance rate. You can start with three iterations and increase this number if the acceptance rates do not approximate the value you set above.

This algorithm is based on work by Prof. Michael Habeck (see these [two](http://proceedings.mlr.press/v22/habeck12.html) [papers](https://arxiv.org/abs/1504.00053)).
