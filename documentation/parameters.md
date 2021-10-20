# Chainsal job parameters

Chainsail is currently tailoired towards experienced users and thus has a whole bunch of parameters you can play around with.
This file aims to provide a complete documentation of all of them.
Please note that to understand the function of some of the parameters, some knowledge about Replica Exchange and other Chainsail internals is required.
See the [algorithms in Chainsail](./algorithms/) for relevant documentation. 

## Basic parameters

- **job name:** allows you to more easily distinguish several jobs you might submit
- **number of production samples:** the number of MCMC samples Chainsail will draw from your probability distribution during the production run. Note that Chainsail currently subsamples to every 5th MCMC sample: if you enter, say, 20,000 here, your downloaded results will contain 4,000 samples for every replica. _Default:_ 10,000
- **maximum number of replicas:** Chainsail will increase (or decrease) the number of replicas automatically such that the acceptance rate between neighboring replicas is approximately constant (by default, 0.2). If your sampling problem is very hard, obtaining these acceptance rates might require a lot of replicas. This parameter defines the upper limit of the number of replicas. If the schedule tuning algorithm thinks that more replicas than that are required, it will stop adapting, use the maximum number of replicas and interpolate the temperature schedule such that acceptance rates are still constant, but lower than the target acceptance rate. Best start with the default value and increase if the maximum is hit and acceptance rates are too low. _Default:_ 20
- **probability definition:** this is a URL to a .zip file containing your `probability.py` Python module (see steps 3-7 of the [walkthrough](./walkthrough.md)
- **dependencies:** a comma-separated list of `pip`-installable Python dependencies your `probability.py` might require

## Advanced parameters

- **initial number of replicas:** the number of replicas the schedule tuning algorithm starts out with. If you have a rough idea of how many (or few) replicas you need, adapt this to save time and computation cost. _Default:_ 5
- **number of optimization samples:** Chainsail performs several schedule optimization runs, the samples of which it uses to estimate the schedule of the next iteration. This sets the number of samples drawn in these optimization runs. It should probably be lower or at most the same number as the number of production samples. _Default:_ 5000
- **tempered distribution family:** no choice here for now, as we support only one
- **beta min:** the only family of tempered distributions we currently support has the form `p(x|beta)=p(x)^beta`, where `p(x)` is your original probability distribution. `beta` is in the range between 0 and 1, so the smaller the minimum `beta`, the flatter the flattest version of your distribution is and the easier to sample it is. Set this to, say, 0.001 if you suspect incorrect sampling in spite of good acceptance rates. _Default_: 0.01
- **target acceptance rate:** Chainsail tries find a temperature schedule such that the acceptance rate between neighboring replicas is approximately constant and equal to this value. Too low acceptance rate hinder efficient sampling and too high acceptance rates potentially waste resources. Optimum values of around 0.2 float around the literature. _Default:_ 0.2 
