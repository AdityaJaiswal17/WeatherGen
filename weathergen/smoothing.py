import numpy as np


def transition_matrix(counts, k=0.0) -> np.ndarray:

    """ Turns the transition counts into probabilities, with k smoothing.

    Parameters
    -----------
    counts : arrays, from transition_count.
    k : float (smoothing parameter), can not be negative.

    Returns
    --------
    numpy.ndarray of float with same shape as counts.
        Each row sums to one, that is the layout and design of this function.

    Raises
    -------
    ValueError : If k is negative or if k is 0 and certain row sums upto 0.
    """

    counts = np.array(counts)
    if k < 0:
        raise ValueError(
            "K is negative, please fix it.")

    if k == 0:
        for row in range(counts.shape[0]):
            if counts[row].sum() == 0:
                raise ValueError(
                    f"Row {row} has all entries as 0.")

    P = (counts + k) / (counts + k).sum(axis=1, keepdims=True)

    return P
