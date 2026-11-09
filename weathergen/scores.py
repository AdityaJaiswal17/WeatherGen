import numpy as np


from .counts import transition_counts
from .simulate_files import check_transition_matrix


def log_likelihood(states, P):

    """ Calculates the Log Likelihood.

    Parameters
    -----------
    states: array, int, 0 for dry, 1 for wet, -1 for missing.
    P: transition matrix. all row values sum to 1

    Returns
    --------
    float
        LL
    """

    P = check_transition_matrix(P)
    order = int(np.log2(P.shape[0]))
    counts = transition_counts(states, order)

    if np.any(P[counts > 0] == 0):
        return -np.inf
    return float(np.sum(counts[counts > 0] * np.log(P[counts > 0])))


def perplexity(states, P):

    """ Calculates the Perpelxity.

    Parameters
    -----------
    states: array, int, 0 for dry, 1 for wet, -1 for missing.
    P: transition matrix. all row values sum to 1

    Returns
    --------
    float
        PPL
    """

    P = check_transition_matrix(P)
    order = int(np.log2(P.shape[0]))

    n_transitions = transition_counts(states, order).sum()
    if n_transitions == 0:
        raise ValueError("Perpelxity is undefined")

    ll = log_likelihood(states, P)
    if ll == -np.inf:
        return np.inf
    return float(np.exp(-ll / n_transitions))
