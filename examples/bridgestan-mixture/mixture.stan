parameters {
  real y;
}
model {
  target += log_sum_exp(log(0.3) + normal_lpdf(y | -1.5, 0.5),
                        log(0.7) + normal_lpdf(y | 2.0, 0.2));
}
