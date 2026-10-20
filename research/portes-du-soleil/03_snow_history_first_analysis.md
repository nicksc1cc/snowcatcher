# Snow history: first analysis

Data: Open-Meteo historical weather API, ERA5 model, daily snowfall, rain and mean temperature from 1950 to May 2026, retrieved 20 October 2026. Season = 1 November to 30 April. Files: `data/snow_era5_seasons.csv`, `data/snow_era5_weekly_median_1991_2020.csv`, `data/snow_era5_summary.json`.

**Read this first.** These are modelled values for one ERA5 grid cell of roughly 25 km that covers the whole domain. Points requested at Les Gets, Avoriaz and Châtel returned identical numbers, so the analysis separates elevations, not sectors. Open-Meteo adjusts temperature to the requested height, and snowfall changes with it; the exact method should be confirmed with the provider. No figure here is a measurement at a piste, and none should be published until checked against stations (section 4).

## 1. Seasonal snowfall by height

| | 1,100 m | 1,600 m | 2,100 m |
|---|---|---|---|
| Median, 1991 to 2020 | 116 cm | 285 cm | 314 cm |
| Middle half of seasons (25th to 75th percentile) | 87 to 140 cm | 261 to 315 cm | 281 to 355 cm |
| Median, 1961 to 1990 | 173 cm | 343 cm | 368 cm |
| Median, 2011 to 2025 | 109 cm | 266 cm | 295 cm |
| Trend 1950 to 2025 (Theil-Sen) | minus 11 cm a decade | minus 10 cm a decade | minus 7 cm a decade |
| Days with 1 cm or more, median | 25 | 50 | 53 |
| Days with 10 cm or more, median | 2 | 8 | 8 |
| First day with 5 cm, median | 29 days after 1 Nov | 13 days after 1 Nov | 10 days after 1 Nov |

## 2. Rain and warmth

| | 1,100 m | 1,600 m | 2,100 m |
|---|---|---|---|
| Rain, December to March, median 1991 to 2020 | 354 mm | 183 mm | 170 mm |
| Rain days (1 mm or more), December to March, median | 36 | 25 | 23 |
| Mean December to February temperature, median 1991 to 2020 | minus 1.6 C | minus 4.8 C | minus 8.1 C |

Winter temperature in the cell has risen by about 0.34 C a decade since 1950, and December to March rain by 10 to 16 mm a decade.

## 3. Poor seasons

A poor season here is one below the 1991 to 2020 lower quartile.

| | 1,100 m | 1,600 m | 2,100 m |
|---|---|---|---|
| Poor seasons, 1950/51 to 1990/91 | 4 of 41 | 8 of 41 | 10 of 41 |
| Poor seasons, 1991/92 to 2025/26 | 11 of 35 | 13 of 35 | 13 of 35 |
| Lowest seasons | 1963/64, 2022/23, 2019/20, 2024/25 | 1963/64, 2022/23, 1956/57 | 1963/64, 1956/57, 1992/93, 2022/23 |
| Last five seasons (2021/22 to 2025/26) | 110, 44, 61, 52, 98 cm | 244, 150, 239, 197, 256 cm | 268, 185, 281, 237, 281 cm |

At 1,100 m, all of the last five seasons fell in the lowest third of the 76 season record (below 112 cm). At 2,100 m the same five seasons ranged from 185 to 281 cm, all below the full record median of 327 cm but much less far below it.

## 4. What this means, and what it does not

* **Height matters more than place.** On the model, a skier at 1,600 m sees more than twice the snowfall of a village at 1,100 m and about a third as many rain days. That supports the sector matrix's focus on lift top and base heights.
* **Low villages are the weak point.** The village returns of Morzine (about 1,000 m), Les Gets (about 1,170 m), Champéry (about 1,050 m), Châtel (about 1,200 m) and the pass only resorts are where the modelled loss is largest. skiresort.com notes that the main link runs have snowmaking; the share by sector is still to be sourced.
* **Not yet shown:** differences between sectors at the same height, aspect, snow depth on the ground, and how often the lifts actually ran. These need ERA5-Land, station data and operator records.

## 5. Next steps

1. Pull ERA5-Land snow depth for the three or four 0.1 degree cells over the domain (blocked during this pass by the API's hourly limit).
2. Identify measuring stations within 15 km: SLF IMIS stations on the Swiss side, Météo-France Nivôse and climatological stations on the French side; compare their snow depth with ERA5-Land by elevation.
3. Confirm with Open-Meteo how snowfall is adjusted for elevation.
4. Decide on licensing (Open-Meteo paid plan or the Copernicus CDS) before any public use.
