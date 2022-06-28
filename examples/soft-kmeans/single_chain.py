from typing import List
import numpy as np
import sys
from rwmc import RWMCSampler
from probability import pdf, initial_states

def sample_single_chain(
        n_samples: int = 10000,
        initial_states: np.ndarray = initial_states,
    ) -> List[np.ndarray]:
    """
    Samples a probability distribution function using a simple, single MCMC chain.
    
    Args:
        n_samples: Number of samples to generate.
        initials_states: Sarting position of the MCMC chain.
    
    Returns:
        A list of samples as numpy.ndarray
    """
    np.random.seed(1)
    initial_states = initial_states.squeeze()
    sampler = RWMCSampler(pdf, initial_states, 0.2)
    samples = []
    accepted = 0
    for i in range(n_samples):
        samples.append(sampler.sample())
        # Counter
        if i % 1000 == 0 and i > 1:
            print("Samples: {}/{} ### Acceptance rate: {:.2f}".format(
                i, n_samples, sampler.acceptance_rate))
    samples = np.array(samples)
    # Save data
    filename = "sc_samples.npy"
    print(f"Saving samples in `{filename}`")
    np.save(filename, samples)
    # Return
    return samples
