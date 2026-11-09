import numpy as np
import pandas as pd

import weathergen

DATES = ["2025-01-01", "2025-01-02", "2025-01-04",
         "2025-01-05", "2025-01-06"]
RAIN = [0.0, 3.0, 4.0, 0.0, 2.0]


class TestFit:
    """Fitting a chain straight from a rainfall DataFrame."""

    def test_spec_example(self):
        """No row for 3 January, so 2 Jan to 4 Jan is not a transition."""
        df = pd.DataFrame({"date": DATES, "rain_mm": RAIN})
        result = weathergen.fit(df)
        assert np.array_equal(result, [[0, 1], [1, 0]])
