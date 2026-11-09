# Oxford daily rainfall, 1827-2025

`oxford_rain.csv` holds the daily rainfall measured at the Radcliffe Meteorological Station, Oxford, from
1 January 1827 to 31 December 2025.

| | |
|---|---|
| Columns | `date` (YYYY-MM-DD) and `rain_mm` (millimetres, one decimal place) |
| Period | 1827-01-01 to 2025-12-31 (199 complete years) |
| Rows | 72,684: one per calendar day, none left out |
| Missing days | 87 (empty `rain_mm`), in 37 gaps; all between March 2022 and December 2025 |
| Longest gap | 6 days (28 June to 3 July 2025) |
| Missing days by year | 2022: 17, 2023: 9, 2024: 28, 2025: 33 |
| Wet days (at least 1.0 mm) | 22,336 of the 72,597 measured days (30.8%) |
| Wettest day | 87.9 mm on 10 July 1968 |

## Reading it

The file has a row for every calendar day, in order, so the `rain_mm` column is the daily record as it stands.

**With NumPy** (Lecture 2, *File operations*), which is all you need until Thursday:

```python
import numpy as np

rain = np.genfromtxt("data/oxford_rain.csv", delimiter=",", skip_header=1, usecols=1)
dates = np.genfromtxt("data/oxford_rain.csv", delimiter=",", skip_header=1, usecols=0, dtype=str)
```

`rain` is a float array of the 72,684 daily totals, with `NaN` for the 87 missing days, and `dates` holds the dates
as strings.

**With pandas**, which is what `fit` uses. Lecture 8, on Thursday, covers reading data this way and working with
dates, so don't worry if this is new for now:

```python
import pandas as pd

df = pd.read_csv("data/oxford_rain.csv", parse_dates=["date"])
```

The empty values become `NaN` here too.

## Source

- **Dataset:** NOAA's Global Historical Climatology Network - Daily (GHCN-Daily), version 3.35-upd-2026100717.
- **Station:** `UK000056225`, OXFORD (51.7667 N, 1.2667 W, 63 m above sea level), the Radcliffe Meteorological
  Station. GHCN-Daily received this station's values from the European Climate Assessment & Dataset (ECA&D):
  every value used here has source flag `E`.
- **File:** <https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/UK000056225.csv.gz>, downloaded on
  9 October 2026 (SHA-256 `ea1d25b01732065728e68f09fbfa82e728c6a3dfb64fe44c7589d3a7339fdc40`).

## How the file was made

1. Keep the `PRCP` rows of the station file (daily precipitation, in tenths of a millimetre).
2. Treat a value that has a quality flag (`Q_FLAG`) as missing. (None of the values used here has one, and none
   has a measurement flag.)
3. Keep the days up to 31 December 2025, the last complete year when the file was made.
4. Write one row per calendar day from the first date to the last, with the value divided by 10 (so in
   millimetres, to one decimal place as in the source), and leave `rain_mm` empty on a day with no value.

Nothing is filled in or invented: a day is missing exactly when GHCN-Daily has no value for it. Up to March 2022
the record has no gaps; the 87 missing days are all in the last four years.

## Licence and attribution

GHCN-Daily is distributed free of charge by NOAA's National Centers for Environmental Information, which asks
users to cite it. The values for this station come from ECA&D, whose data policy allows their use in
non-commercial research and education, with the acknowledgement below. The file is provided for this module's
coursework on those terms: use it for your coursework and your own learning, and don't use it commercially.

- Menne, M.J., I. Durre, B. Korzeniewski, S. McNeill, K. Thomas, X. Yin, S. Anthony, R. Ray, R.S. Vose,
  B.E. Gleason, and T.G. Houston, 2012: Global Historical Climatology Network - Daily (GHCN-Daily), Version 3
  (3.35-upd-2026100717). NOAA National Climatic Data Center. doi:10.7289/V5D21VHZ. Accessed 9 October 2026.
- Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical
  Climatology Network-Daily Database. *Journal of Atmospheric and Oceanic Technology*, 29, 897-910,
  doi:10.1175/JTECH-D-11-00103.1.
- We acknowledge the data providers in the ECA&D project. Klein Tank, A.M.G. and Coauthors, 2002. Daily dataset
  of 20th-century surface air temperature and precipitation series for the European Climate Assessment.
  *International Journal of Climatology*, 22, 1441-1453. Data and metadata available at <https://www.ecad.eu>.
