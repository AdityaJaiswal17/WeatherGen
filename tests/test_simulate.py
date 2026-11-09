import time

import numpy as np
import pytest

import weathergen


class TestSimulateLoop:
    """Sampling days from a transition matrix with plain loops."""

    def test_spec_example(self):
        """The table in the specs: seed 2 gives wet, wet, dry, wet."""
        P = [[0.7, 0.3], [0.4, 0.6]]
        result = weathergen.simulate_loop(P, 4, np.random.default_rng(2))
        assert np.array_equal(result, [[1, 1, 0, 1]])

    def test_shape_and_integers(self):
        """Always 2-D (n_realisations, n_days) and integer states."""
        P = [[0.7, 0.3], [0.4, 0.6]]
        rng = np.random.default_rng(0)
        result = weathergen.simulate_loop(P, 5, rng, n_realisations=3)
        assert result.shape == (3, 5)
        assert result.dtype.kind == "i"

    def test_initial_sets_the_first_context(self):
        """P flips the weather every day, so the start decides it all."""
        P = [[0, 1], [1, 0]]
        rng = np.random.default_rng(0)
        default = weathergen.simulate_loop(P, 4, rng)
        after_wet = weathergen.simulate_loop(P, 4, rng, initial=[1])
        assert np.array_equal(default, [[1, 0, 1, 0]])
        assert np.array_equal(after_wet, [[0, 1, 0, 1]])

    def test_order_two_reads_oldest_day_first(self):
        """After (dry,dry) or (dry,wet) it is wet, otherwise dry."""
        P = [[0, 1], [0, 1], [1, 0], [1, 0]]
        result = weathergen.simulate_loop(P, 8, np.random.default_rng(0))
        assert np.array_equal(result, [[1, 1, 0, 0, 1, 1, 0, 0]])

    def test_invalid_matrix_raises(self):
        """Rows must sum to 1 and there must be 2, 4, 8, ... of them."""
        rng = np.random.default_rng(0)
        with pytest.raises(ValueError):
            weathergen.simulate_loop([[0.5, 0.4], [0.4, 0.6]], 5, rng)
        with pytest.raises(ValueError):
            weathergen.simulate_loop([[0.5, 0.5]] * 3, 5, rng)


class TestSimulate:
    """The fast version has to match the loop version exactly."""

    def test_same_as_simulate_loop(self):
        """Same seed and same matrix give the same days."""
        P = [[0.1, 0.9], [0.5, 0.5], [0.8, 0.2], [0.3, 0.7]]
        slow = weathergen.simulate_loop(
            P, 30, np.random.default_rng(7), 20, initial=[1, 0])
        fast = weathergen.simulate(
            P, 30, np.random.default_rng(7), 20, initial=[1, 0])
        assert np.array_equal(slow, fast)

    def test_at_least_five_times_faster(self):
        """The specs: 1000 realisations of 1000 days, 5x faster."""
        P = [[0.7, 0.3], [0.4, 0.6]]
        start = time.perf_counter()
        weathergen.simulate_loop(P, 1000, np.random.default_rng(0), 1000)
        slow_time = time.perf_counter() - start
        start = time.perf_counter()
        weathergen.simulate(P, 1000, np.random.default_rng(0), 1000)
        fast_time = time.perf_counter() - start
        assert slow_time >= 5 * fast_time
