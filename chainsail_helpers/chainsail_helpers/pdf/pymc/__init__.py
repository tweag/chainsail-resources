"""
Interfaces for Chainsail probability densities defined by a PyMC model
"""

from functools import reduce
from itertools import accumulate
from operator import mul

from chainsail_helpers.pdf import PDF


class PyMCPDF(PDF):
    """
    Chainsail PDF wrapper around a PyMC (https://docs.pymc.io) model.
    """

    def __init__(self, model):
        """
        Initializes a Chainsail-compatible PDF wrapper around a PyMC model.

        Args:
            model(pymc.Model): PyMC model
        """
        self._model = model
        self._logp_function = model.compile_logp()
        self._dlogp_function = model.compile_dlogp()
        self._rv_ranges_shapes = self._make_rv_range_shape_dict()

    def _make_rv_range_shape_dict(self):
        """
        Build a dictionary that contains, for each random variable,
        the range of indices of in the flat coordinate array that contain
        that random variable's value and its shape, so we can reconstruct
        a dictionary of random variables for consumption by
        self._logp_function and self._dlogp_function
        """
        rv_shapes = self._model.eval_rv_shapes()
        sorted_rvs = sorted(rv_shapes.keys())
        sorted_rv_shapes = {var: rv_shapes[var] for var in sorted_rvs}
        flat_lengths = (reduce(mul, shape, 1)
                        for shape in sorted_rv_shapes.values())
        offsets = [0] + list(accumulate(flat_lengths))
        return {var: ((offsets[i], offsets[i + 1]), rv_shapes[var])
                for i, var in enumerate(sorted_rvs)}

    def _flat_to_var_dict(self, x):
        return {var: x[from_index:to_index].reshape(shape) for
                var, ((from_index, to_index), shape)
                in self._rv_ranges_shapes.items()}

    def log_prob(self, x):
        """
        Log-probability of the density to be sampled.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              is evaluated. This is the concatenation of the flattened values
              of all PyMC model variables in alphabetical order, so if you have
              two variables var1 and var2 with shapes (2, 2) and (3,), x is
              (in pseudo code) (x1, x2, x3, x4, x5, x6, x7) with
              (x1, ..., x4) = var1.flatten() and
              (x5, ..., x7) = var2.flatten().

        Returns:
            float: log-probability evaluated at x
        """
        return float(self._logp_function(self._flat_to_var_dict(x)))

    def log_prob_gradient(self, x):
        """
        Gradient of the log-probability of the density to be sampled.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              gradient is evaluated. This is the concatenation of the flattened
              values of all PyMC model variables in alphabetical order, so if
              you have two variables var1 and var2 with shapes (2, 2) and (3,),
              x is (in pseudo code) (x1, x2, x3, x4, x5, x6, x7) with
              (x1, ..., x4) = var1.flatten()
              and (x5, ..., x7) = var2.flatten().

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        return self._dlogp_function(self._flat_to_var_dict(x))
