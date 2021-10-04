"""
Interfaces for Chainsail probability densities defined by a PyMC3 model
"""

from chainsail_helpers.pdf import PDF


class PyMC3PDF(PDF):
    """
    Chainsail PDF wrapper around a PyMC3 (https://docs.pymc.io) model.
    """

    def __init__(self, model):
        """
        Initializes a Chainsail-compatible PDF wrapper around a PyMC3 model.

        Args:
            model(pymc3.model.Model): PyMC3 model
        """
        self.logp_dlogp_function = model.logp_dlogp_function()
        self.logp_dlogp_function.set_extra_values({})

    def log_prob(self, x):
        """
        Log-probability of the density to be sampled.
        Wraps around the logp_dlogp_function function of a PyMC3 model.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              is evaluated

        Returns:
            float: log-probability evaluated at x
        """
        return self.logp_dlogp_function(x)[0]

    def log_prob_gradient(self, x):
        """
        Gradient of the log-probability of the density to be sampled.
        Wraps around the logp_dlogp_function function of a PyMC3 model.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              gradient is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        return self.logp_dlogp_function(x)[1]
