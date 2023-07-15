# Example: sampling from a mixture distribution using the BridgeStan wrapper

This provides a very minimal example of how to define a Chainsail-compatible `probability.py` that uses a Stan model in a separate file and the BrideStan wrapper from the `chainsail-helpers` library.
Note that when creating a ZIP archive with `probability.py`, you'll have to add `mixture.stan` to it, too, for example using
```console
zip probability.zip probability.py mixture.stan
```
