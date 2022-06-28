'''
A simple Metropolis-Hastings sampler for demo purposes
'''
import numpy as np


class RWMCSampler:
    def __init__(self, pdf, state, stepsize):
        self.pdf = pdf
        self.state = state
        self.stepsize = stepsize
        self._n_moves_accepted = 0
        self._n_moves = 0

    @property
    def acceptance_rate(self):
        return self._n_moves_accepted / self._n_moves if self._n_moves else 0.0

    def sample(self):
        E_old = -self.pdf.log_prob(self.state)
        proposal = self.state + np.random.uniform(
            low=-self.stepsize, high=self.stepsize, size=len(self.state))
        E_new = -self.pdf.log_prob(proposal)

        accepted = np.log(np.random.random()) < -(E_new - E_old)

        if accepted:
            self.state = proposal
            self._n_moves_accepted += 1

        self._n_moves += 1

        return self.state.copy()
