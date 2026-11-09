import numpy as np

from weathergen import wet_days


def test_wet_at_or_above_threshold():
    """A day is wet if rain >= threshold: 1.0 mm is wet by default."""
    rain = [0.0, 0.5, 1.0, 3.2]
    assert np.array_equal(wet_days(rain), [0, 0, 1, 1])


def test_nan_is_missing():
    """Unrecorded data (no rainfall measurement) is assigned -1."""
    rain = [0.0, np.nan, 2.0, 3.0]
    assert np.array_equal(wet_days(rain), [0, -1, 1, 1])


def test_states_are_integers():
    """ To check whether the output of wet_days is an
        array of integers -- {0, 1, -1} """
    rain = [0.0, 0.5, 1.0, 3.2, np.nan]
    states = wet_days(rain)
    # States is an np.ndarray, all the elements in it are of the same data type
    assert states.dtype == int


def test_changing_threshold():
    """ Threshold can be changed and this should not
        break the code, checking for this """
    assert np.array_equal(wet_days([0.4, 0.5, 0.6], threshold=0.5), [0, 1, 1])


def test_empty_input_gives_empty_array():
    """ No rain therefore no states out. """
    assert wet_days([]).tolist() == []


def test_input_is_not_modified():
    """ The input is not modified by the operations """
    rain = np.array([0.0, np.nan, 2.0])
    before = rain.copy()
    wet_days(rain)
    assert np.array_equal(rain, before, equal_nan=True)
