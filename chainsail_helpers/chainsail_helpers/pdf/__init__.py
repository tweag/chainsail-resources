"""
Abstract PDF interfaces for Chainsail
"""
from abc import abstractmethod, ABCMeta


class PDF(ABCMeta):
    """
    Minimal interface general probability densities consumed by Chainsail have
    to conform to.
    """

    @abstractmethod
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

    @abstractmethod
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


class PosteriorPDF(PDF):
    """
    Interface for posterior probability densities consumed by Chainsail
    """
    @abstractmethod
    def log_likelihood(self, x):
        """
        Log-likelihood function of the model.

        Args:
            x(np.ndarray): 1D array of floats at which the log-likelihood
              function is evaluated

        Returns:
            float: log-likelihood function evaluated at x
        """
        pass

    @abstractmethod
    def log_likelihood_gradient(self, x):
        """
        Gradient of the log-likelihood function of the model.

        Args:
            x(np.ndarray): 1D array of floats at which the gradient of the
              log-likelihood function is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-likelihood function gradient evaluated at x
        """
        pass

    @abstractmethod
    def log_prior(self, x):
        """
        Log-prior of the model.

        Args:
            x(np.ndarray): 1D array of floats at which the log-prior
              is evaluated

        Returns:
            float: log-prior evaluated at x
        """
        pass

    @abstractmethod
    def log_prior_gradient(self, x):
        """
        Gradient of the log-prior of the model.

        Args:
            x(np.ndarray): 1D array of floats at which the gradient of the
              log-prior is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-prior gradient evaluated at x
        """
        pass

    def log_prob(self, x):
        """
        Log-posterior density to be sampled.

        Args:
            x(np.ndarray): 1D array of floats at which the log-posterior
              is evaluated

        Returns:
            float: log-posterior evaluated at x
        """
        return self.log_likelihood(x) + self.log_prior(x)

    def log_prob_gradient(self, x):
        """
        Gradient of the log-posterior of the density to be sampled.

        Args:
            x(np.ndarray): 1D array of floats at which the log-posterior
              gradient is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-posterior gradient evaluated at x
        """
        return self.log_likelihood_gradient(x) + self.log_prior_gradient(x)
