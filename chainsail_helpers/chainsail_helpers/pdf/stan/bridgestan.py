"""
Wrappers for Chainsail probability densities defined by a Stan model, using BridgeStan
"""

import json
from typing import Any

import numpy as np
import bridgestan as bs


class BridgeStanPDF:
    """
    Chainsail PDF wrapper around BridgeStan (https://github.com/roualdes/bridgestan).
    """

    def __init__(self, model_file: str, data: dict[str, Any] | None=None) -> None:
        """
        Initializes a Chainsail-compatible PDF wrapper around the BridgeStan API.

        Args:
            model_file: path to a Stan model file
            data(dict): observations to condition on
        """
        data = data or {}
        self._model = bs.StanModel.from_stan_file(model_file, json.dumps(data))


    def log_prob(self, x: np.ndarray) -> float:
        """
        Log-probability of the density to be sampled.
        Calls out to the httpstan server specified in self._httpstan_url.
        Args:
            x: 1D array of floats at which the log-probability
              is evaluated

        Returns:
            log-probability evaluated at x
        """
        return self._model.log_density(x, jacobian=False)

    def log_prob_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Gradient of the log-probability of the density to be sampled.

        Args:
            x: 1D array of floats at which the log-probability
              gradient is evaluated

        Returns:
            1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        _, gradient = self._model.log_density_gradient(x, jacobian=False)
        return gradient
