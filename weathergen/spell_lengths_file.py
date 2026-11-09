import numpy as np


def spell_lengths(states, value):

    """ Maximal length of a continuos spell.

    Parameters
    ----------
    states : array, int, 0 for dry, 1 for wet, -1 for missing.
    value : int, 0 for dry spells or 1 for wet spells.

    Returns
    -------
    numpy.ndarray of int
        The length of each complete spell, in the order they occur.

    Raises
    ------
    ValueError : If value is not 0 or 1.
    """

    if value not in [0, 1]:
        raise ValueError("value must be either 0 (dry) or 1 (wet)")

    states = np.array(states)
    len_states = len(states)
    lengths = []
    i = 0

    while i < len_states:
        if states[i] != value:
            i += 1
            continue

        start = i
        while i < len_states and states[i] == value:
            i += 1
        end = i

        touches_start = start == 0
        touches_end = end == len_states

        if touches_start or touches_end:
            continue

        if states[start - 1] == -1 or states[end] == -1:
            continue

        lengths.append(end - start)

    return np.array(lengths, dtype=int)
