import numpy as np
import pandas as pd

import weathergen

df = pd.read_csv("data/oxford_rain.csv")
real_states = weathergen.wet_days(df["rain_mm"].to_numpy())

# real record
real_spells = weathergen.spell_lengths(real_states, 0)
real_long = np.sum(real_spells >= 30)
real_years = len(real_states) / 365.25
print("real record:", real_long / real_years, "per year")

# simulations: one long record of 2000 years for each order
n_years = 2000
rng = np.random.default_rng(1)

for order in [1, 6]:
    P = weathergen.fit(df, order=order, k=0.5)
    sim = weathergen.simulate(P, n_years * 365, rng)[0]
    sim_spells = weathergen.spell_lengths(sim, 0)
    sim_long = np.sum(sim_spells >= 30)
    print("order", order, ":", sim_long / n_years, "per year")
