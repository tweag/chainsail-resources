# Defining your own probability distribution

The [`chainsail-helpers` package](./chainsail_helpers/README.md) provides the abstract interface (in [`chainsail_helpers.pdf`](./chainsail_helpers/chainsail_helpers/pdf/__init__.py). You have three options:
   - code up your probability distribution yourself by subclassing either the general PDF or the posterior PDF interface. In that case, make sure to specify any Python dependencies you might require during the job submission step.
   - in case you happen to already have your statistical model formulated in [PyMC](https://docs.pymc.io), you can use the [PyMC wrapper](./chainsail_helpers/chainsail_helpers/pdf/pymc/__init__.py). An example is provided [here](./examples/pymc-mixture/probability.py).
   - if you formulated your model in [Stan](https://mc-stan.org), use the [Stan wrapper](./chainsail_helpers/chainsail_helpers/pdf/stan/__init__.py) we provide. It talks to a Chainsail-internal [`httpstan`](https://github.com/stan-dev/httpstan) server and might thus be a bit slow. Also see the [example](./examples/stan-mixture/probability.py).

Follow these steps when defining your own probability distribution:
1. make an instance of your PDF available as an object with name `pdf` in a file called `probability.py` and furthermore provide a flat `numpy` array called `initial_states` in the same file which holds the initial state for the MCMC samplers. Note that all Python dependencies you use have to be entered into the corresponding field on the job submission form. Chainsail comes with a couple of standard dependencies preinstalled:
   - `numpy` (version 1.23.2),
   - `scipy` (version 1.9.1),
   - `pymc` (version 4.1.7),
   - `chainsail-helpers` (version 0.1.4)
2. test whether your PDF implementation actually works by calling its `log_{prob / likelihood, prior}` and `log_{prob / likelihood, prior}_gradient` methods with your `initial_states` as an argument. We will provide an automated way to easily test this later.
3. prepare a zip file of your `probability.py` and any other file dependencies your code may have (e.g., data files) and make sure that you don't have subdirectories and that this structure matches how you access these files in your `probability.py`.
4. upload that zip file in the job submission form.
