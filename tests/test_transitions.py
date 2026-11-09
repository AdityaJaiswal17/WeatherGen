import numpy as np

import weathergen
import pytest

states = [0, 1, 1, 0, -1, 1, 0, 0, 1]


class TestTransitionCounts:

    """Counting day-to-day moves into a (2**order, 2) table."""

    def test_simple_sequence_order_one(self):
        """ 0->1, 1->1, 1->0: trivial """
        counts = weathergen.transition_counts([0, 1, 1, 0], order=1)
        assert np.array_equal(counts, [[0, 1], [1, 1]])

    def test_spec_example_order_one(self):
        """ Test whether the function works for order 1. """
        counts = weathergen.transition_counts(states, order=1)
        assert np.array_equal(counts, [[1, 2], [2, 1]])

    def test_spec_example_order_two(self):
        """ Test whether function works for order 2. """
        counts = weathergen.transition_counts(states, order=2)
        assert np.array_equal(counts, [[0, 1], [0, 1], [1, 0], [1, 0]])

    def test_too_short_gives_all_zeros(self):
        """ Record shorter than order is invalid, give all days 0. """
        counts = weathergen.transition_counts([0, 1], order=2)
        assert np.array_equal(counts, np.zeros((4, 2)))


class TestTransitionMatric:

    """ Counts to probabilities, testing the function here. """

    def test_spec_example(self):
        """ Test against the examples given in the specs.md """
        result = weathergen.transition_matrix([[1, 2], [2, 1]])
        expected = np.array([[1 / 3, 2 / 3], [2 / 3, 1 / 3]])
        assert result == pytest.approx(expected)

    def test_negative_k_is_rejected(self):
        """ Negative smoothing could make probabilities negative. """
        counts = [[1, 2], [2, 1]]
        with pytest.raises(ValueError):
            weathergen.transition_matrix(counts, k=-1)

    def test_unseen_context_without_smoothing_is_rejected(self):
        """ A row of zeros with k=0 has no probabilities: name the row. """
        counts = [[1, 2], [0, 0]]
        with pytest.raises(ValueError, match=r"(?i)(row|context) 1"):
            weathergen.transition_matrix(counts)

    def test_unseen_context_with_smoothing_is_computed(self):
        """ With k > 0 a never-seen row is not an error: it is 50/50. """
        counts = [[1, 2], [0, 0]]
        result = weathergen.transition_matrix(counts, k=1)
        assert result.shape == (2, 2)
        assert not np.isnan(result).any()
        assert result[0] == pytest.approx([0.4, 0.6])
        assert result[1] == pytest.approx([0.5, 0.5])
        assert result.sum(axis=1) == pytest.approx(1.0)
