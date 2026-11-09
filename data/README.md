# Oxford daily rainfall, 1827-2025

The results in the main README use the daily rainfall measured at the Radcliffe Meteorological Station, Oxford, from
1 January 1827 to 31 December 2025. The data comes from NOAA (see *Getting the data*).

## The file

`data/oxford_rain.csv`, one row per calendar day, in order:

| | |
|---|---|
| Columns | `date` (YYYY-MM-DD) and `rain_mm` (millimetres, one decimal place) |
| Period | 1827-01-01 to 2025-12-31 (199 complete years) |
| Rows | 72,684, one per calendar day |
| Missing days | 87 (empty `rain_mm`), all between March 2022 and December 2025; the longest gap is 6 days |
| Wet days (at least 1.0 mm) | 22,336 of the 72,597 measured days (30.8%) |

These figures are for GHCN-Daily version 3.35-upd-2026100717. NOAA updates the dataset regularly, so a newer
download may differ slightly, mostly in the recent years.

## Getting the data

The data comes from NOAA's Global Historical Climatology Network - Daily (GHCN-Daily), station `UK000056225`
(OXFORD, 51.7667 N, 1.2667 W, 63 m above sea level):
<https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/UK000056225.csv.gz>

`oxford_rain.csv` keeps the daily precipitation (`PRCP`) values, converted from tenths of a millimetre to
millimetres, with one row per calendar day up to 31 December 2025. A value with a quality flag counts as missing.

Nothing is filled in: a day is missing exactly when GHCN-Daily has no value for it. `weathergen` marks those days
as missing, so they break the chain instead of being counted as dry.

## Reading it

```python
import pandas as pd

df = pd.read_csv("data/oxford_rain.csv", parse_dates=["date"])
```

Missing days come through as `NaN`.

## Licence and attribution

GHCN-Daily is distributed free of charge by NOAA's National Centers for Environmental Information. The values for
this station come from the European Climate Assessment & Dataset (ECA&D), whose data policy allows use in
non-commercial research and education with the acknowledgement below. This project uses the data on those terms.

- Menne, M.J., I. Durre, B. Korzeniewski, S. McNeill, K. Thomas, X. Yin, S. Anthony, R. Ray, R.S. Vose,
  B.E. Gleason, and T.G. Houston, 2012: Global Historical Climatology Network - Daily (GHCN-Daily), Version 3.
  NOAA National Climatic Data Center. doi:10.7289/V5D21VHZ.
- Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical
  Climatology Network-Daily Database. *Journal of Atmospheric and Oceanic Technology*, 29, 897-910,
  doi:10.1175/JTECH-D-11-00103.1.
- We acknowledge the data providers in the ECA&D project. Klein Tank, A.M.G. and Coauthors, 2002. Daily dataset
  of 20th-century surface air temperature and precipitation series for the European Climate Assessment.
  *International Journal of Climatology*, 22, 1441-1453. Data and metadata available at <https://www.ecad.eu>.
