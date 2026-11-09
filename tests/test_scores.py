import numpy as np
import pytest


import weathergen


states = [0, 1, 1, 0, -1, 1, 0, 0, 1]
P = [[1 / 3, 2 / 3], [2 / 3, 1 / 3]]
FAIR = [[0.5, 0.5], [0.5, 0.5]]
BAD = [[0.5, 0.4], [0.4, 0.6]]


class TestLogLikelihood:
    """Log-likelihood of a record under a transition matrix."""

    def test_spec_example(self):
        """The spec's record scores about -3.819."""
        result = weathergen.log_likelihood(states, P)
        assert result == pytest.approx(-3.819, abs=1e-3)

    def test_no_transitions_gives_zero(self):
        """One day has no transition, so the sum is empty."""
        assert weathergen.log_likelihood([0], P) == 0.0

    def test_impossible_transition_gives_minus_infinity(self):
        """Going 0 to 1 when P says it never happens gives -inf."""
        result = weathergen.log_likelihood([0, 1], [[1, 0], [0, 1]])
        assert result == -np.inf

    def test_hundred_years_is_finite(self):
        """36500 days: adding logs works, multiplying would hit zero."""
        states = [0, 1] * 18250
        result = weathergen.log_likelihood(states, FAIR)
        assert result == pytest.approx(36499 * np.log(0.5))

    def test_invalid_matrix_raises(self):
        """Rows that do not sum to 1 are rejected."""
        with pytest.raises(ValueError):
            weathergen.log_likelihood(states, BAD)


class TestPerplexity:
    """Perplexity: the average surprise per transition."""

    def test_spec_example(self):
        """The spec's record has perplexity about 1.890."""
        result = weathergen.perplexity(states, P)
        assert result == pytest.approx(1.890, abs=1e-3)

    def test_fair_coin_gives_two(self):
        """Every probability 0.5 is a coin flip, so perplexity is 2."""
        result = weathergen.perplexity([0, 1, 1, 0, 1], FAIR)
        assert result == pytest.approx(2.0)

    def test_impossible_transition_gives_infinity(self):
        """A log-likelihood of -inf means perplexity inf."""
        result = weathergen.perplexity([0, 1], [[1, 0], [0, 1]])
        assert result == np.inf

    def test_no_transitions_raises(self):
        """With nothing to average over, perplexity is undefined."""
        with pytest.raises(ValueError):
            weathergen.perplexity([0], P)

    def test_invalid_matrix_raises(self):
        """Rows that do not sum to 1 are rejected."""
        with pytest.raises(ValueError):
            weathergen.perplexity(states, BAD)
