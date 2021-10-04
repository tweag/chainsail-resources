# Chainsail PDF interfaces and utilities

This small package complements the [Chainsail](https://chainsail.io) sampling service. It
- defines the general interface for objects representing Chainsail-consumable probability distributions,
- provides implementations thereof for popular probabilistic programming languages,
- and contains a few helper scripts for post-processing.

## Installation
This package requires a few Python dependencies.
Best use [Poetry](https://python-poetry.org) to install them and develop your own probability density implementation: run
```bash
$ poetry install
$ poetry shell
```
and you will be dropped into a virtual environment with these dependencies installed.
If you'd like implement a probability density using [Stan](https://mc-stan.org) or [PyMC3](https://docs.pymc.io), install the corresponding extra dependencies like so: `poetry install --extras pymc3` and similarly for `stan`. 
When using Chainsail, this package will be automatically installed, so no need to add it to the list of dependencies in the job submission form.

## Contributing
Contributions, for example PDF implementations for other probabilistic programming languages, are highly welcome!
Just open a pull request and we'll be happy to work with you to make Chainsail even more useful.

## License
&copy; 2021 [Tweag](https://tweag.io). `chainsail_helpers` is open-source software and licensed under the [MIT license](https://opensource.org/licenses/MIT).
