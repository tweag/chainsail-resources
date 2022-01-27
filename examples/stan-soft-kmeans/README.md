# Soft k-means clustering, with Stan and Chainsail
This is an example of using Chainsail for soft k-means clustering, as it is defined in the [Stan user guide](https://mc-stan.org/docs/2_21/stan-users-guide/soft-k-means.html).


You can directly check out the jupyter notebook where all analyses were made. It can be run with Nix (instructions for installing Nix [here](https://nixos.org/manual/nix/unstable/installation/installing-binary.html))
```bash
nix-shell shell-jupyter.nix --command "jupyter notebook soft-kmeans.ipynb"
```


This clustering example includes the following steps:
- **Data generation**
  The clustered data `data.txt` was simulated using the `make_data.py` script, that can be run using the Nix shell `shell-dev.nix`.
  ```bash
  nix-shell shell-dev.py --command "python make_data.py data.txt"
  ```
- **Model definition in Stan**
  The model for clustering is defined in in `stan-model.txt`. It is a bivariate Gaussian mixture, and was taken from the [Stan soft k-means example](https://mc-stan.org/docs/2_21/stan-users-guide/soft-k-means.html)
- **Posterior sampling with Stan**
  The posterior distribution was first sampled with Rstan, using a single Hamiltonian Monte Carlo chain. See `soft-kmeans.ipynb`.
- **Posterior sampling with Chainsail**
  And the posterior distribution was also sampled with Chainsail. The `probability.py` uses the [chainsail_helpers](https://github.com/tweag/chainsail-resources/tree/main/chainsail_helpers) package, to wrap around the Stan model, and expose the log probability and log probability gradient of the model for Chainsail. The results of the run are in `run_chainsail`.
- **Comparison the 2 sampling methods**
  See `soft-kmeans.ipynb`.
