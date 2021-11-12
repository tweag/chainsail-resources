# Postprocessing scripts
This contains scripts we offer to the user to simplify working with the simulation results.

## Concatenate samples
`concatenate_samples.py` is a script that extracts the samples for the first replica from a Chainsail run result and concatenates them into a single `numpy` array. Call it like so:
```bash
$ concatenate-samples --simulation_run /path/to/run_directory --out target_samples.npy
```
A run directory would for example be `production_run` or `optimization_run1`.
