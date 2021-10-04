"""
Abstract PDF interfaces for Chainsail
"""


class PDF:
    """
    Minimal interface all probability densities consumed by Chainsail have
    to conform to.
    """

    def log_prob(self, x):
        """
        Log-probability of the density to be sampled.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              is evaluated

        Returns:
            float: log-probability evaluated at x
        """
        pass

    def log_prob_gradient(self, x):
        """
        Gradient of the log-probability of the density to be sampled.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              gradient is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        pass
