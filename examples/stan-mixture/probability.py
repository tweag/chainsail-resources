"""
Probability density of a Gaussian mixture defined by a Stan model
"""

import numpy as np

from chainsail_helpers.pdf.stan.httpstan import BaseStanPDF

model_code = """
parameters {
  real y;
}
model {
  target += log_sum_exp(log(0.3) + normal_lpdf(y | -1.5, 0.5),
                        log(0.7) + normal_lpdf(y | 2.0, 0.2));
}
"""

pdf = BaseStanPDF(model_code)
initial_states = np.array([np.random.uniform(-2, 3)])
