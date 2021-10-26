# How to use Chainsail

1. sign up on the [Chainsail website](https://chainsail.io) by clicking the "Login" button or directly [this link](https://resaas-simeon-dev.ey.r.appspot.com/login)
2. [write us an email](mailto:support@chainsail.io) so we can authorize your account to use the computing resources
3. implement the probability distribution you want to sample. The [`chainsail-helpers` package](./chainsail_helpers/README.md) provides the abstract interface (in [`chainsail_helpers.pdf`](./chainsail_helpers/chainsail_helpers/pdf/__init__.py). You have three options:
   - code up your probability distribution yourself by subclassing the abstract interface. In that case, make sure to specify any Python dependencies you might require during the job submission step.
   - in case you happen to already have your statistical model formulated in [PyMC3](https://docs.pymc.io), you can use the [PyMC3 wrapper](./chainsail_helpers/chainsail_helpers/pdf/pymc3/__init__.py). An example is provided [here](./examples/pymc3-mixture/probability.py).
   - if you formulated your model in [Stan](https://mc-stan.org), use the [Stan wrapper](./chainsail_helpers/chainsail_helpers/pdf/stan/__init__.py) we provide. It talks to a Chainsail-internal [`httpstan`](https://github.com/stan-dev/httpstan) server and might thus be a bit slow. Also see the [example](./examples/stan-mixture/probability.py).
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
