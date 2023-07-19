"""
Sample probability distribution definition using the BridgeStan wrapper
and a Stan model defined in `mixture.stan`
"""

import numpy as np

from chainsail_helpers.pdf.stan.bridgestan import BridgeStanPDF

pdf = BridgeStanPDF("mixture.stan")
initial_states = np.array([[1.0]])
