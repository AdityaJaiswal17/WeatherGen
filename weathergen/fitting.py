import pandas as pd

from .states import wet_days
from .counts import transition_counts
from .smoothing import transition_matrix


def fit(df, order=1, k=0.0, threshold=1.0):

    """
    Fits a transition matrix to a DataFrame of daily rainfall.

    Parameters
    ----------
    df : DataFrame with columns 'date' and 'rain_mm'.
    order : int, how many previous days make up the context.
    k : float, smoothing, as in transition_matrix.
    threshold : float, a day is wet if rain_mm >= threshold.

    Returns
    -------
    numpy.ndarray of float with shape (2**order, 2).

    Notes
    -----
    a date with no row counts as a missing day, so it breaks the chain.
    """

    dates = pd.to_datetime(df["date"])
    rain = pd.Series(df["rain_mm"].to_numpy(dtype=float), index=dates)

    daily = pd.date_range(rain.index.min(), rain.index.max(), freq="D")
    rain = rain.reindex(daily)

    states = wet_days(rain.to_numpy(), threshold)
    counts = transition_counts(states, order)
    return transition_matrix(counts, k)
