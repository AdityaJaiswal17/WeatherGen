import numpy as np


def check_transition_matrix(P):

    """ Checks whether P passes the convention
        test as defined in the specs.md """

    P = np.asarray(P, dtype=float)
    n_rows = P.shape[0]
    # Bitwise check for power of 2
    if n_rows & (n_rows - 1) != 0 or P.shape[1] != 2:
        raise ValueError(
            "Transition matrix is invalid and must have 2 columns."
            )

    if not np.all(abs(P.sum(axis=1) - 1) < 1e-9):
        raise ValueError(
            "Transition matrix is invalid and is not within tolerance."
            )

    return P


def starting_context(initial):

    """
    Gives the starting context based on the 'initial' input.

    Context refers to the row here.
    """

    if initial is None:
        return 0

    else:
        context = 0
        for i in initial:
            context = context * 2 + i
        return context


def simulate_loop(P, n_days, rng, n_realisations=1, initial=None):

    """ Runs the simulate loop.

    Parameters
    -----------
    P: transition matrix
    n_days: number of days taken into consideration
    rng: random number generator
    n_realisations: kind of samples that are drawn, represented by rows
    initial: the states before the day 0

    Returns
    --------
    The simulated values which dictates the wet and dry states.
    """

    P = np.asarray(P, dtype=float)
    u = rng.random((n_realisations, n_days))
    P = check_transition_matrix(P)
    start = starting_context(initial)

    result = np.zeros((n_realisations, n_days), dtype=int)
    for r in range(n_realisations):
        context = start
        for t in range(n_days):
            if u[r, t] < P[context, 1]:
                day_state = 1
            else:
                day_state = 0

            result[r, t] = day_state
            context = (context * 2 + day_state) % P.shape[0]
    return result


def simulate(P, n_days, rng, n_realisations=1, initial=None):

    """ Runs the simulate.
    Gives exactly the same result as simulate_loop.py.
    But everything exacted at once so this verison is supposed to be faster..

    Parameters
    -----------
    P: transition matrix
    n_days: number of days taken into consideration
    rng: random number generator
    n_realisations: kind of samples that are drawn, represented by rows
    initial: the states before the day 0

    Returns
    --------
    The simulated values which dictates the wet and dry states.
    """

    P = np.asarray(P, dtype=float)
    u = rng.random((n_realisations, n_days))
    P = check_transition_matrix(P)
    start = starting_context(initial)

    context = np.full(n_realisations, start, dtype=int)
    result = np.zeros((n_realisations, n_days), dtype=int)

    for t in range(n_days):
        day_state = (u[:, t] < P[context, 1])
        result[:, t] = day_state
        context = (context * 2 + day_state) % P.shape[0]
    return result
