import pandas as pd

import weathergen

df = pd.read_csv("data/oxford_rain.csv")
train = df[df["date"] <= "1990-12-31"]
test = df[df["date"] >= "1991-01-01"]
test_states = weathergen.wet_days(test["rain_mm"].to_numpy())

print("order  k=0.0  k=0.5")
for order in range(1, 13):
    results = []
    for k in [0.0, 0.5]:
        try:
            P = weathergen.fit(train, order=order, k=k)
            results.append(weathergen.perplexity(test_states, P))
        except ValueError:
            # k=0 and some pattern was never seen in training
            results.append(float("nan"))
    print(order, results[0], results[1])
