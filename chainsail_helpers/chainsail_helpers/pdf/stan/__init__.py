"""
Interfaces for Chainsail probability densities defined by a Stan model
"""
from __future__ import annotations

import functools
from typing import Any, Callable

import numpy as np
import requests

from chainsail_helpers.pdf import PDF


class BaseStanPDF(PDF):
    """
    Chainsail PDF wrapper around httpstan
    (https://github.com/stan-dev/httpstan).
    """
    _HTTPSTAN_URL = "http://localhost:8082"

    def __init__(self, model_code: str, data: dict[str, Any] | None=None) -> None:
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

    def _query_log_prob(self, x: np.ndarray,
                        preflight_data_transform: Callable | None=None) -> float:
        """
        Uses the httpstan HTTP API to evaluate the model's log-probability.

        Args:
            x: 1D array of floats at which the log-likelihood is evaluated
            preflight_data_transform: transformation to be applied to the data
              before sending it to httpstan

        Returns:
            log-probability evaluated at `x`
        """
        try:
            if preflight_data_transform:
                data = preflight_data_transform(self._data)
            else:
                data = self._data
            r = requests.post(
                f"{self._httpstan_model_route}/log_prob",
                json={
                    "unconstrained_parameters": x.tolist(),
                    "data": data,
                    "adjust_transform": False,
                },
            )
            r.raise_for_status()
            return r.json()["log_prob"]
        except Exception as e:
            raise Exception(f"Querying log-prob failed: Error: {e}")

    def _query_log_prob_gradient(self, x: np.ndarray, preflight_data_transform: Callable | None=None) -> np.ndarray:
        """
        Uses the httpstan HTTP API to evaluate the model's log-probability gradient.

        Args:
            x: 1D array of floats at which the log-probability's gradient is evaluated
            preflight_data_transform: transformation to be applied to the data
              before sending it to httpstan

        Returns:
            1D array with log-probability gradient evaluated at `x`
        """
        try:
            if preflight_data_transform:
                data = preflight_data_transform(self._data)
            else:
                data = self._data
            r = requests.post(
                f"{self._httpstan_model_route}/log_prob_grad",
                json={
                    "unconstrained_parameters": x.tolist(),
                    "data": data,
                    "adjust_transform": False,
                },
            )
            r.raise_for_status()
            return np.array(r.json()["log_prob_grad"])
        except Exception as e:
            raise Exception(f"Querying log-prob gradient failed: Error: {e}")

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
        return self._query_log_prob(x)

    def log_prob_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Gradient of the log-probability of the density to be sampled.
        Calls out to the httpstan server specified in self._httpstan_url.

        Args:
            x: 1D array of floats at which the log-probability
              gradient is evaluated

        Returns:
            1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        return self._query_log_prob_gradient(x)


class PosteriorStanPDF(BaseStanPDF):
    """
    Chainsail PDF wrapper around httpstan
    (https://github.com/stan-dev/httpstan).
    """
    _HTTPSTAN_URL = "http://localhost:8082"

    def __init__(self, model_code: str, data: dict[str, Any] | None=None) -> None:
        """
        Initializes a Chainsail-compatible, likelihood-temperable PDF wrapper around
        the httpstan REST API.

        The Stan model has to take the additional "data" in the `data` section:
        ```
        int<lower=0, upper=1> include_prior ;
        int<lower=0, upper=1> include_likelihood ;
        ```

        and in the `model` section, these values need to be used to conditionally switch
        on and off the prior and likelihood contributions, like so:

        ```
        if (include_prior) {
            param_a ~ SomeDistribution ;
            param_b ~ SomeOtherDistribution ;
        } ;

        if (include_likelihood) {
            data ~ YetAnotherDistribution(param_a, param_b)
        } ;
        ```

        Args:
            model_code(string): Stan model specification that will be compiled
              by httpstan
            data(dict): observations to condition on
        """
        super().__init__(model_code, data)

    @staticmethod
    def _tag_data(data: dict[str, Any], include_prior: bool=True, include_likelihood: bool=True) -> dict[str, Any]:
        """
        Adds tags / flags to the data that indicate whether the prior or likelihood should be included.
        Args:
            data: observations to condition on
            include_prior: whether the prior contributions are taken into account in later log-probability
              or gradient evaluations
            include_likelihood: whether the likelihood is taken into account in later log-probability
              or gradient evaluations

        Returns:
            data dictionary with additional entries `include_prior` and `include_likelihood`, set to either
              0 or 1.
        """
        return {**data,
                "include_prior": int(include_prior),
                "include_likelihood": int(include_likelihood)}

    def log_likelihood(self, x: np.ndarray) -> float:
        """
        Evaluates the log-likelihood of the model.
        
        Calls out to the httpstan server specified in self._httpstan_url with
        datums `include_prior` set to `0` and `include_likelihood` set to `1`.

        Args:
            x: 1D array of floats at which the log-likelihood
              is evaluated

        Returns:
            log-likelihood evaluated at x
        """
        preflight_data_transform = functools.partial(self._tag_data, include_prior=False)
        return self._query_log_prob(x, preflight_data_transform)

    def log_prior(self, x: np.ndarray) -> float:
        """
        Evaluates the log-prior probability of the model.
        
        Calls out to the httpstan server specified in self._httpstan_url with
        datums `include_prior` set to `1` and `include_likelihood` set to `0`.

        Args:
            x: 1D array of floats at which the log-prior probability
              is evaluated

        Returns:
            log-prior probability evaluated at x
        """
        preflight_data_transform = functools.partial(self._tag_data, include_likelihood=False)
        return self._query_log_prob(x, preflight_data_transform)
    
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
        return self._query_log_prob(x)

    def log_likelihood_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Evaluates the gradient of the log-likelihood of the model.
        Calls out to the httpstan server specified in self._httpstan_url
        with datums `include_prior` set to `0` and `include_likelihood` set to `1`.

        Args:
            x: 1D array of floats at which the gradient of the
              log-likelihood is evaluated

        Returns:
            1D array of floats containing the flattened
              gradient of the log-likelihood evaluated at x
        """
        preflight_data_transform = functools.partial(self._tag_data, include_prior=False)
        return self._query_log_prob_gradient(x, preflight_data_transform)

    def log_prior_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Evaluates the gradient of the log-prior density of the model.
        Calls out to the httpstan server specified in self._httpstan_url
        with datums `include_prior` set to `1` and `include_likelihood` set to `0`.

        Args:
            x: 1D array of floats at which the gradient of the
              log-prior density is evaluated

        Returns:
            1D array of floats containing the flattened
              gradient of the log-prior density evaluated at x
        """
        preflight_data_transform = functools.partial(self._tag_data, include_likelihood=False)
        return self._query_log_prob_gradient(x, preflight_data_transform)
        
    def log_prob_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Gradient of the log-probability of the density to be sampled.
        Calls out to the httpstan server specified in self._httpstan_url.

        Args:
            x: 1D array of floats at which the log-probability
              gradient is evaluated

        Returns:
            1D array of floats containing the flattened
              log-probability gradient evaluated at x
        """
        return self._query_log_prob_gradient(x)
