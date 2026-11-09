import time

import numpy as np

import weathergen

P = [[0.7, 0.3], [0.4, 0.6]]
sizes = [100, 300, 1000, 2000]

print("size  loop  simulate  speedup")
for size in sizes:
    # same number of days and realisations, same seed for both
    start = time.perf_counter()
    weathergen.simulate_loop(P, size, np.random.default_rng(0), size)
    loop_time = time.perf_counter() - start

    start = time.perf_counter()
    weathergen.simulate(P, size, np.random.default_rng(0), size)
    fast_time = time.perf_counter() - start

    print(size, loop_time, fast_time, loop_time / fast_time)
