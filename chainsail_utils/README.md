# Chainsail PDF interfaces and utilities

This small package
- defines the general interface for objects representing Chainsail-consumable probability distributions,
- implementations thereof for popular probabilistic programming languages,
- and a few helper scripts for post-processing.

## Installation
This package requires a few Python dependencies.
Best use [Poetry](https://python-poetry.org) to install them and develop your own probability density implementation: run
```bash
$ poetry install
$ poetry shell
```
and you will be dropped into a virtual environment with these dependencies installed.
When using Chainsail, this package will be automatically installed, so no need to add it to the list of dependencies in the job submission form.

## Contributing
Contributions like PDF implementations for other probabilistic programming languages are highly welcome!
Just open a pull request and we'll be happy to work with you to make Chainsail even more useful.

## License
&copy; 2021 [Tweag][https://tweag.io]. `chainsail_utils` is open-source software and licensed under the [MIT license](https://opensource.org/licenses/MIT).
