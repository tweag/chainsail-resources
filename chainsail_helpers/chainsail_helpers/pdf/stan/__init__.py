"""
Interfaces for Chainsail probability densities defined by a Stan model
"""

import numpy as np
import requests

from chainsail_helpers.pdf import PDF


class StanPDF(PDF):
    """
    Chainsail PDF wrapper around httpstan
    (https://github.com/stan-dev/httpstan).
    """
    _HTTPSTAN_URL = "http://localhost:8082"

    def __init__(self, model_code, data=None):
        """
        Initializes a Chainsail-compatible PDF wrapper around the httpstan
        REST API.

        Args:
            model_code(string): Stan model specificaton that will be compiled
              by httpstan
            data(dict): observations to condition on
        """
        r = requests.post(
            f"{self._HTTPSTAN_URL}/v1/models",
            json={"program_code": model_code},
        )
        # if the model did not compile successfully, httpstan returns
        # a 400 status code (bad request)
        if r.status_code == 400:
            raise Exception(
                ("Model compilation failed. httpstan message:\n"
                 f"{r.json()['message']}")
            )
        else:
            r.raise_for_status()
        model_id = r.json()["name"]
        self._httpstan_model_route = f"{self._HTTPSTAN_URL}/v1/{model_id}"
        self._data = data or {}

    def log_prob(self, x):
        """
        Log-probability of the density to be sampled.
        Calls out to the httpstan server specified in self._httpstan_url.
        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              is evaluated

        Returns:
            float: log-probability evaluated at x
        """
        try:
            r = requests.post(
                f"{self._httpstan_model_route}/log_prob",
                json={
                    "unconstrained_parameters": x.tolist(),
                    "data": self._data,
                    "adjust_transform": False,
                },
            )
            r.raise_for_status()
            return r.json()["log_prob"]
        except Exception as e:
            raise Exception(f"Querying log-prob failed: Error: {e}")

    def log_prob_gradient(self, x):
        """
        Gradient of the log-probability of the density to be sampled.
        Calls out to the httpstan server specified in self._httpstan_url.

        Args:
            x(np.ndarray): 1D array of floats at which the log-probability
              gradient is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        try:
            r = requests.post(
                f"{self._httpstan_model_route}/log_prob_grad",
                json={
                    "unconstrained_parameters": x.tolist(),
                    "data": self._data,
                    "adjust_transform": False,
                },
            )
            r.raise_for_status()
            return np.array(r.json()["log_prob_grad"])
        except Exception as e:
            raise Exception(f"Querying log-prob gradient failed: Error: {e}")
