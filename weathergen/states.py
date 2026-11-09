import numpy as np


def wet_days(rain, threshold=1.0) -> np.ndarray:

    """
    Daily rainfall totals (mm) to states: 1 wet, 0 dry, -1 missing.

    Parameters
    ----------
    rain : array of float, daily rainfall in mm, NaN if missing.
    threshold : float, a day is wet if rain >= threshold.

    Returns
    -------
    numpy.ndarray of int, same length as rain.
    """

    rain = np.asarray(rain, dtype=float)
    states = (rain >= threshold).astype(int)
    states[np.isnan(rain)] = -1
    return states
