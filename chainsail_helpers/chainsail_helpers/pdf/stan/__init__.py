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

    @staticmethod
    def _tag_data(data, include_prior, include_likelihood):
        return {**data,
                "include_prior": int(include_prior),
                "include_likelihood": int(include_likelihood)}

    def _query_log_prob(self, x, include_prior=True, include_likelihood=True):
        try:
            r = requests.post(
                f"{self._httpstan_model_route}/log_prob",
                json={
                    "unconstrained_parameters": x.tolist(),
                    "data": self._tag_data(self._data, include_prior, include_likelihood),
                    "adjust_transform": False,
                },
            )
            r.raise_for_status()
            return r.json()["log_prob"]
        except Exception as e:
            raise Exception(f"Querying log-prob failed: Error: {e}")

    def _query_log_prob_gradient(self, x, include_prior=True, include_likelihood=True):
        try:
            r = requests.post(
                f"{self._httpstan_model_route}/log_prob_grad",
                json={
                    "unconstrained_parameters": x.tolist(),
                    "data": self._tag_data(self._data, include_prior, include_likelihood),
                    "adjust_transform": False,
                },
            )
            r.raise_for_status()
            return np.array(r.json()["log_prob_grad"])
        except Exception as e:
            raise Exception(f"Querying log-prob gradient failed: Error: {e}")

    def log_likelihood(self, x):
        """
        Evaluates the log-likelihood of the model.
        
        Calls out to the httpstan server specified in self._httpstan_url with
        datums `include_prior` set to `0` and `include_likelihood` set to `1`.

        Args:
            x(np.ndarray): 1D array of floats at which the log-likelihood
              is evaluated

        Returns:
            float: log-likelihood evaluated at x
        """
        return self._query_log_prob(x, include_prior=False)

    def log_prior(self, x):
        """
        Evaluates the log-prior probability of the model.
        
        Calls out to the httpstan server specified in self._httpstan_url with
        datums `include_prior` set to `1` and `include_likelihood` set to `0`.

        Args:
            x(np.ndarray): 1D array of floats at which the log-prior probability
              is evaluated

        Returns:
            float: log-prior probability evaluated at x
        """
        return self._query_log_prob(x, include_likelihood=False)
    
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
        return self._query_log_prob(x)

    def log_likelihood_gradient(self, x):
        """
        Evaluates the gradient of the log-likelihood of the model.
        Calls out to the httpstan server specified in self._httpstan_url
        with datums `include_prior` set to `0` and `include_likelihood` set to `1`.

        Args:
            x(np.ndarray): 1D array of floats at which the gradient of the
              log-likelihood is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              gradient of the log-likelihood evaluated at x
        """
        return self._query_log_prob_gradient(x, include_prior=False)

    def log_prior_gradient(self, x):
        """
        Evaluates the gradient of the log-prior density of the model.
        Calls out to the httpstan server specified in self._httpstan_url
        with datums `include_prior` set to `1` and `include_likelihood` set to `0`.

        Args:
            x(np.ndarray): 1D array of floats at which the gradient of the
              log-prior density is evaluated

        Returns:
            np.ndarray: 1D array of floats containing the flattened
              gradient of the log-prior density evaluated at x
        """
        return self._query_log_prob_gradient(x, include_likelihood=False)
        
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
        return self._query_log_prob_gradient(x)
