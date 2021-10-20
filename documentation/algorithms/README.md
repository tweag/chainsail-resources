# Chainsail algorithms

Chainsail implements several important algorithms, which we describe here in not too much detail:
- [Replica Exchange](./replica_exchange.md): Chainsail's main ingredient that allows you to sample multimodal probability distributions
- [Automatic Replica Exchange tuning](./schedule_tuning): Replica Exchange requires setting a kind of "temperature" schedule, which Chainsail automatically determines for you
- [Hamiltonian Monte Carlo](./hmc.md): While Replica Exchange takes care of _global_ sampling, meaning it helps to discover all modes of your probability distribution, _local_ sampling algorithms like Hamiltonian Monte Carlo sample well within a single mode.
