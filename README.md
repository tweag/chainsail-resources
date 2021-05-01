# Chainsail resources and documentation
Examples, documentation and other additional resources related to Chainsail

## Chainsail: a web service to sample multimodal probability distributions
Chainsail is a web service which helps you sample from multimodal probability distributions. In the context of Bayesian statistics, they arise in the case of unidentifiable parameters which are due to some symmetry in the model or if you have ambiguous data.

### The secret ingredient: Replica Exchange
Chainsail is essentially a Replica Exchange ([blog post](https://www.tweag.io/blog/2020-10-28-mcmc-intro-4/)) implementation with automated temperature schedule tuning deployed on a cloud computing platforms to provide the necessary parallel computing power. 
In a nutshell, Replica Exchange is a Markov chain Monte Carlo (MCMC) algorithm that works by simulating a series of increasingly "flatter" versions (_replicas_) of a probability distribution with a "local" MCMC algorithm such as Hamiltonian Monte Carlo ([blog post](https://www.tweag.io/blog/2020-08-06-mcmc-intro3/)) and occasionally exchanging states between all those simulations.
That way, the Markov chain that samples the distribution of interest can escape from modes it is otherwise likely to be trapped in. 
Replica Exchange requires the choice of a series of probability distributions, which interpolate between the target distribution and some very easy to sample, "flat" distribution.
It is convenient to choose a parameterized family of "tempering" distributions and then vary its parameter to set a _schedule_.
The only family of distributions currently implemented is of the form `p(x|beta)=p(x)^beta` with `0 < beta <= 1` and `p(x)` your probability distribution of interest.

### Automated schedule tuning
Chainsail automagically finds appropriate schedules via an iterative algorithm which results in approximatively constant acceptance rates between neighboring distributions.
This algorithm is based on work by Prof. Michael Habeck (see these [two](http://proceedings.mlr.press/v22/habeck12.html) [papers](https://arxiv.org/abs/1504.00053)).

## Usage
To use the current beta version of Chainsail, prerequisites currently are:
- basic understanding of MCMC sampling
- the statistics / math / Python skills to implement the log-probability of your probability distribution and its gradient
- you have contacted the project lead ([Simeon Carstens](mailto:simeon.carstens@tweag.io) to obtain the URL

Chainsail currently implements a naive version of Hamiltonian Monte Carlo (HMC) with only a basic automatic adaption of the integration step size, a unit mass matrix and a fixed number of integration steps per HMC step. 
You have to provide your probability density in the form of a Python module from which an object `Pdf` and a flat `numpy` array `initial_states` can be imported.
The expected interface for the `Pdf` object is described [here](./examples/probability.py).
The user is furthermore expected to set a few essential parameters for sampling and optimization, although somewhat reasonable defaults are given:
- the number of optimization (schedule parameter tuning) runs: the more difficult your sampling problem is, the higher you want to set this
- the number of MCMC samples per optimization run
- the number of MCMC samples in the final production run
- the minimum inverse temperature: this parameter determines the flatness `beta` of the flattest copy of your probability distribution: leave this at the default value or set it to `0.001` if you're not happy with the results
- the initial number of replicas (copies of your distribution): the harder your sampling problem is, the higher you want to set this. The number of replicas will be adapted automatically during a Chainsail run.
- the target Replica Exchange acceptance rate: usually, 0.2 is a good value, but if your sampling problem is very difficult, you can set this to a higher value (but <1), just to be safe

Also make sure to add all Python dependencies your `probability.py` module requires as a comma-separated list into the corresponding field in the job submission form.

Once you click on "Submit job", you will be redirected to a table listing all your sampling jobs. Start your new job by clicking the corresponding button in your job's row. 
You can now monitor the progress of your job in the dashboard, which shows two basic statistics to assess convergence and whether the schedule optimization works. 
Once your job is finished, the dashboard and the job table will display a link to a `.zip` file containing all your sampling results.
Once downloaded and extracted, you can use a little [postprocessing script](./postprocessing/concatenate_samples.py) to stitch together batches of samples into one big `numpy` array.

And finally, don't forget to send us your [feedback](mailto:simeon.carstens@tweag.io) :-)

## Questions?
Shoot us an [email](mailto:simeon.carstens@tweag.io)!
