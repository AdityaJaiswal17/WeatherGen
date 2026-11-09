import numpy as np


def transition_counts(states: np.ndarray, order=1) -> np.ndarray:

    """ Counts how often each outcome follows each context in wet/dry days.

    Parameters
    -----------
    states : array, 0 for dry, 1 for wet, -1 for missing.
    order : int, how many previous days are taken in consideration.

    Returns
    --------
    numpy.ndarray of int with shape (2**order, 2).
        counts[i, j] is how often outcome j (0 dry, 1 wet) came after
        context i. The context is the previous `order` days read as a
        binary number, oldest day first, so for order 2 (dry, wet) is
        row 1 and (wet, dry) is row 2.

    Notes
    -----
    A transition is only counted if all order + 1 days are present, so a
    missing day breaks the chain. A record shorter than order + 1 days
    gives all zeros.
    """

    states = np.array(states)
    counts = np.zeros((2 ** order, 2), dtype=int)
    n_windows = len(states) - order
    if n_windows <= 0:
        return counts

    windows = np.column_stack(
        [states[k:k + n_windows] for k in range(order + 1)])
    windows = windows[(windows >= 0).all(axis=1)]

    context = np.zeros(len(windows), dtype=int)
    for k in range(order):
        context = context * 2 + windows[:, k]

    np.add.at(counts, (context, windows[:, order]), 1)
    return counts
