# weathergen

A small, tested python package that forms a wet/dry markov chain from daily rainfall data and simulates the new predicted rainfall.

## What it does

A day is wet if it has atleast 1mm of rainfall (this is the default et threshold, this can be changed as well). In a chain of order n, the chance that today is wet depends only on whether each of the previous n days was wet or dry. `weathergen` counts those patterns in a real record (`transition_counts`), turns the counts into probabilities with optional smoothing (`transition_matrix`), and simulates new records from them (`simulate_loop`, and the faster `simulate`, which give exactly the same answer). Days with no measurement are marked as missing and break the chain instead of being counted as dry. It can also score a record under a chain (`log_likelihood`, `perplexity`), measure the length of complete dry or wet spells (`spell_lengths`), and fit a chain straight from a table of daily rainfall (`fit`).

## Installing and running

```
conda env create -f environment.yml
conda activate weathergen
pytest
flake8 .
```

An example:

```python
import numpy as np
import pandas as pd
from weathergen import fit, simulate

df = pd.read_csv("data/oxford_rain.csv")
P = fit(df, order=2)
days = simulate(P, 365, np.random.default_rng(1), n_realisations=10)
```

The above sets up and activates the environment.

## Choosing the order

I fitted order from 1 to 12 on Oxford record up to 1990 and scored them on 1991 onward. Lower perplexity is obviously better.

| order | k = 0 | k = 0.5 |
|---|---|---|
| 1 | 1.802574 | 1.802574 |
| 2 | 1.787190 | 1.787189 |
| 3 | 1.783426 | 1.783426 |
| 4 | 1.781970 | 1.781969 |
| 5 | 1.781337 | 1.781333 |
| **6** | **1.780581** | **1.780569** |
| 7 | 1.782270 | 1.782237 |
| 8 | 1.784411 | 1.784297 |
| 9 | 1.790444 | 1.789986 |
| 10 | 1.799706 | 1.797672 |
| 11 | inf | 1.812973 |
| 12 | undefined | 1.837307 |

I would use order 6, which has the lowest perplexity. Orders 3 to 6 are fairly close. After Order 6 it starts getting worse and 11 gives infinite perplexity while order 12 can not be fitted at all. Smoothing with k = 0.5 also almost changes nothing, it makes orders 11 and 12 work but certainly order 6 is the best order to be chosen.

## Speed

Run times are in second recorded using time module. The function times were measured using time.perf_counter(). Each is timed once so the numbers can be misleading but carry the general sentiment throughout.

| days | realisations | simulate_loop (s) | simulate (s) | speed-up |
|---|---|---|---|---|
| 100 | 100 | 0.02867 | 0.003457 | 8.29 |
| 300 | 300 | 0.11993 | 0.012384 | 9.68 |
| 1000 | 1000 | 0.850 | 0.039388 | 21.58 |
| 2000 | 2000 | 2.5815 | 0.29755 | 8.675 |

`simulate_loop` takes longer time because of the for loop overhead at every step. Hence, the `simulate` was always faster.

## One finding

I counted the complete dry spells of 30 days per year in the real Oxford record, and in 2000 simulated years from a chain of order 1 as well as order 6 (the one most optimal and chosen above), each smoothed with k = 0.5.

| | dry spells of 30+ days per year |
|---|---|
| Real record (1827 to 2025) | 0.231 |
| Order 1 (2000 simulated years) | 0.026 |
| Order 6 (2000 simulated years) | 0.198 |

As evident from the above simulated values, the order of 6 gets very close to the actual real record. 

## Reproducing these

Create and activate the environment first (see *Installing and running*), then run each script from repo.

| Section | Script | Command |
|---|---|---|
| Choosing the order | `scripts/choose_order.py` | `python scripts/choose_order.py` |
| Speed | `scripts/time_simulate.py` | `python scripts/time_simulate.py` |
| One finding | `scripts/dry_spells.py` | `python scripts/dry_spells.py` |
