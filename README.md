# Chainsail resources and documentation
Examples, documentation and other additional resources related to Chainsail

## Chainsail: a web service to sample multimodal probability distributions
Chainsail is a web service which helps you sample from multimodal probability distributions. In the context of Bayesian statistics, they arise in the case of unidentifiable parameters which are due to some symmetry in the model or if you have ambiguous data.


## Usage
Learn how to use Chainsail in only 13 steps :-)
Don't worry, it's not as complicated as it sounds.
If you have any questions, don't hesitate to [shoot us a message](mailto:support@chainsail.io)!

1. sign up on the [Chainsail website](https://chainsail.io) by clicking the "Login" button or directly [this link](https://resaas-simeon-dev.ey.r.appspot.com/login)
2. [write us an email] so we can authorize your account to use the computing resources
3. implement the probability distribution you want to sample. The [`chainsail-helpers` package](./chainsail_helpers/README.md) provides the abstract interface (in [`chainsail_helpers.pdf`](./chainsail_helpers/chainsail_helpers/pdf/__init__.py). You have three options:
   - code up your probability distribution yourself by subclassing the the abstract interface. In that case, make sure to specify any Python dependencies you might require during the job submission step.
   - in case you happen to already have your statistical model formulated in [PyMC3](https://docs.pymc.io), you can use the [PyMC3 wrapper](./chainsail_resources/chainsail_resources/pdf/pymc3/__init__.py). An example is provided [here](./examples/pymc3-mixture/probability.py).
   - if you formulated your model in [Stan](https://mc-stan.org), use the [Stan wrapper](./chainsail_resources/chainsail_resources/pdf/stan/__init__.py) we provide. It talks to a Chainsail-internal [`httpstan`](https://github.com/stan-dev/httpstan) server and might thus be a bit slow.
4. make an instance of your PDF available as an object with name `pdf` in a file called `probability.py` and furthermore provide a flat `numpy` array called `initial_states` in the same file which holds the initial state for the MCMC samplers
5. test whether your PDF implementation actually works by calling `pdf.log_prob` and `pdf.log_prob_gradient` with your `initial_states` as an argument. We will provide an automated way to easily test this later.
6. prepare a zip file of your `probability.py` and any other file dependencies your code may have (e.g., data files) and make sure that you don't have subdirectories and that this structure matches how you access these files in your `probability.py`.
7. upload that zip file to some publicly accessible URL.
8. create a new sampling job by on the [Chainsail website](https://chainsail.io) by click on "Create new job" and filling out the form. Here's some help for the form fields:
   - Job name: pick any job name you want.
   - Number of production samples: make some kind of estimate of how many samples you want to have produced in the end. Chainsail will produce that number of samples and write out every 5th of these samples.
   - Maximum number of replicas: the higher this number, the better the multimodal sampling will be, but the more computation resources you will burn. Start with the default value of 10 and increase if you suspect that sampling is not correct.
   - Probability definition: enter here the URL to which you uploaded your zipped `probability.py`.
   - Dependencies: using a comma-separated list, enter any PIP-installable Python dependencies your `probability.py` requires.
If you click on "more parameters", you'll find exactly that - they are [documented elsewhere](./docs/parameters.md).
Finally, create your job by clicking the "Create job" button.
9. Start your job by clicking the corresponding button in the job table.
10. Monitor the progress of your job and the log output on the dashboard, which is accessible via the job table, too.
11. Once your job finishes, both the job table and the dashboard will show a "download" button. Clicking on it will download an archive of all the samples.
12. Unpack the downloaded sample archive and use the [sample concatenation script](./chainsail_helpers/scripts/concatenate_samples.py) to concatenate the samples.
13. [Send us feedback](mailto:support@chainsail.io) on whether Chainsail worked for you and how we can improve it :-)

## The algorithms behind Chainsail
Without spilling too many beans of this currently closed-source project, here's some background information for if you're interested what algorithms power Chainsail.

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

### Local sampling using Hamiltionian Monte Carlo
Chainsail currently implements a naive version of Hamiltonian Monte Carlo (HMC) with only a basic automatic adaption of the integration step size, a unit mass matrix and a fixed number of integration steps per HMC step. 
A better local sampling algorithm will be implemented in later stages of the project.



## Questions?
Shoot us an [email](mailto:support@chainsail.io)!
