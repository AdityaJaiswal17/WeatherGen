import numpy as np
import pytest

import weathergen

states = [1, 0, 0, 1, 1, 1, 0, -1, 0, 1, 0, 0, 0, 0, 1]


class TestSpellLengths:
    """Lengths of complete dry or wet spells in a states."""

    def test_spec_example_dry(self):
        """ The spec states has dry spells of 2 and 4 days. """
        result = weathergen.spell_lengths(states, 0)
        assert np.array_equal(result, [2, 4])

    def test_spec_example_wet(self):
        """ The same states has wet spells of 3 and 1 days. """
        result = weathergen.spell_lengths(states, 1)
        assert np.array_equal(result, [3, 1])

    def test_spells_at_start_and_end_are_left_out(self):
        """ The dry runs touching either end of the states are dropped. """
        result = weathergen.spell_lengths([0, 1, 0, 1, 0], 0)
        assert np.array_equal(result, [1])

    def test_spell_next_to_missing_day_is_left_out(self):
        """ The dry run beside the -1 could be longer, so it is dropped. """
        result = weathergen.spell_lengths([1, 0, 0, -1, 1, 0, 1], 0)
        assert np.array_equal(result, [1])

    def test_value_must_be_zero_or_one(self):
        """ Only dry (0) and wet (1) spells exist. """
        with pytest.raises(ValueError):
            weathergen.spell_lengths(states, 2)
