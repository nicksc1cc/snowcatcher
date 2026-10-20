# Snow and weather data: sources, stack and pipeline

Covers deliverables 3 (API and dataset comparison), 4 (pipeline), 5 (historical analysis plan) and 6 (current conditions and forecast plan). Checked 20 October 2026. Terms marked "to confirm" have not been read in full.

## 1. Source comparison

| Source | What it supplies | Coverage and resolution | History | Data type | Access and cost | Commercial use and storage | Verdict |
|---|---|---|---|---|---|---|---|
| Open-Meteo historical weather API (ERA5) | Daily and hourly snowfall, rain, temperature, wind, cloud; temperature adjusted to a requested elevation | Global, 0.25 degree grid (about 25 km). **One ERA5 cell (46.25 N, 6.75 E) covers the whole domain**: three test points 10 km apart returned identical values | 1940 onwards | Modelled reanalysis | Free API: 600 calls a minute, 5,000 an hour, 10,000 a day; a 76 year daily request for 3 variables used most of a minute's quota | Free tier non commercial only. Paid plans include commercial use; the pricing FAQ says historical data needs the Professional plan (the page is inconsistent). Data CC BY 4.0 | Use for long run trends and elevation contrasts, labelled as modelled. Not for sector detail |
| Open-Meteo historical API (ERA5-Land) | Hourly snow depth, snowfall water equivalent, temperature | 0.1 degree grid (about 9 km), so three to four cells across the domain | 1950 onwards | Modelled reanalysis | Same API and quotas | Same terms | Best open source for modelled snow depth; grid elevations differ from piste elevations, and snowfall_sum returned 0 in a test call |
| Open-Meteo forecast API | Snowfall, precipitation, temperature, wind gusts, freezing level, for up to 16 days | Best match picks high resolution models (MeteoSwiss ICON, Météo-France AROME, ECMWF IFS); each requested elevation was matched to a different nearby grid cell | Forecast only | Forecast | Free API, same quotas | Free tier non commercial | Use for the forecast panel, with issue time shown |
| Open-Meteo historical forecast API | Archived forecast runs | As forecast models | From about 2021, varies by model | Archived forecast | Same | Same | Use later for forecast validation |
| Copernicus ERA5-Land (CDS) | Same variables as above, full fields | 0.1 degree | 1950 onwards | Modelled reanalysis | Free account, queued requests, NetCDF or GRIB processing | Copernicus licence allows commercial use with attribution (to confirm wording) | Fallback if Open-Meteo's paid plan is not taken; heavier to process |
| Meteostat | Station daily data including maximum snow depth (`snow`, mm) | Station based; nearest stations to be listed | Decades for some stations | Measured, gaps filled with model data by default (`model=true`) | RapidAPI key; 10 years per request | Licence to confirm (believed non commercial) | Use only with `model=false` and only for stations close in height |
| MeteoSwiss open data | Station measurements, including snow depth at some stations and manual precipitation stations | Swiss stations, a few near the Val d'Illiez to be identified | Decades | Measured | Free open data downloads | Open government data; terms to confirm | Strong candidate for the Swiss side |
| SLF IMIS network | Snow depth, simulated 24 hour new snow, temperature, wind, every 30 minutes | Nearly 200 Swiss stations; stations near the Swiss sectors to be identified | Live via API; older than 7 days via file download | Measured (new snow simulated by SNOWPACK) | Free | Terms of use to read before any public display | Best candidate for measured mountain snow depth on the Swiss side |
| Météo-France climatological data and avalanche bulletin | Station snow depth (Nivôse and manual stations); Chablais avalanche bulletin (BRA) in PDF and XML | French stations; bulletin for the Chablais massif | Decades for stations | Measured; expert bulletin | Météo-France API portal and public data site | Licence Ouverte (to confirm for each product) | Strong candidate for the French side and avalanche data |
| Official domain and resort reports | Lifts and pistes open, reported snow depth at named points | Each resort | Daily, archive not public | Manually reported | Web pages | Display terms to agree with operators | Needed for current conditions; never merged into one domain figure |
| skiresort.com | Snow report summary, past snow depths chart, webcams | Domain level | Some history | Reported, aggregated | Web pages | Third party content, cannot be republished | Corroboration only |

## 2. Recommended starting stack

1. **History:** Open-Meteo ERA5 for seasonal snowfall, rain and temperature at three elevation bands, and ERA5-Land for modelled snow depth at the three or four grid cells that touch the domain. Labelled "modelled" everywhere. A paid Open-Meteo plan, or the Copernicus CDS route, before anything is published on a commercial site.
2. **Measured check:** SLF IMIS and MeteoSwiss stations on the Swiss side, Météo-France stations on the French side, chosen within 15 km and within 300 m of height of the sector they represent. Used to measure the reanalysis bias, not to replace it.
3. **Current conditions:** the official lift and piste status page and each resort's snow report, stored daily with timestamps, plus the avalanche bulletins.
4. **Forecast:** Open-Meteo forecast at low, mid and high points in each zone, with the issue time.

## 3. Pipeline

| Job | Source | Cadence | Stored | Volume (rough) |
|---|---|---|---|---|
| Forecast pull | Open-Meteo forecast, 18 points (6 zones x 3 elevations) | 4 times a day in season | raw JSON + normalised rows | about 2,500 rows a day |
| Snow report scrape | Official status page and 12 resort reports | Daily at 08:30 and 13:00 local | raw HTML snapshot + parsed record per measuring point | about 50 records a day |
| Lift and piste status | Official status page | Every 30 minutes, 08:00 to 17:30 | open or closed per lift | about 4,000 rows a day |
| Station data | IMIS, MeteoSwiss, Météo-France | Daily | raw + normalised | small |
| Avalanche bulletins | Météo-France Chablais, SLF | Daily | danger level by aspect and elevation | small |
| Reanalysis refresh | ERA5, ERA5-Land | After each season | seasonal and weekly statistics | small |

Storage: raw records kept unchanged, normalised records in one long table (schema in 01_methodology_and_schema.md), derived statistics in separate tables with the script version that produced them. A season of all jobs is well under 1 GB.

## 4. Historical analysis plan

* **Units and season:** centimetres for snowfall and depth, millimetres for rain, season 1 November to 30 April, labelled by start year.
* **Points:** low (1,100 m), mid (1,600 m) and high (2,100 m) for each of three zones (Les Gets and Morzine; Avoriaz and Les Crosets; Châtel, Morgins and Torgon). ERA5 cannot separate the zones; ERA5-Land and stations can.
* **Statistics:** median, mean, 10th, 25th, 75th and 90th percentiles for 1991 to 2020; days with 1 cm and 10 cm of new snow; median snowfall by week of season; first day with 5 cm; seasons below the 1991 to 2020 lower quartile, before and after 1991; Theil-Sen trends with the period stated.
* **Snow depth:** days above 30, 50 and 100 cm; depth by week; start and end of continuous cover; low versus high contrast. Modelled depth is shown as a band, never as a piste figure.
* **Checks:** compare ERA5-Land depth with IMIS and Météo-France stations; record the bias by elevation; never present the model as validation of itself.

First results are in 03_snow_history_first_analysis.md.

## 5. Current conditions and forecast plan

* **Each record carries** source, measuring point, elevation, report time, retrieval time and data type. A sector with no report shows "not available".
* **Display:** base, mid and top depth separately, never one domain number; new snow over 24 hours, 48 hours and 7 days only where the source reports it.
* **Forecast panel:** snowfall, freezing level, temperature and gusts at three heights per zone, with the model run time and a line saying it is a forecast.
* **Avalanche:** danger level and the bulletin link for the Chablais (France) and the relevant Valais region (Switzerland).
* **Separation of long term and today:** the page keeps "how reliable is the snow here historically" and "what is it like this week" in different panels.

## 6. Snow reliability measure

No single score yet. The first measure to publish, once station checks are done, is "share of seasons since 1991 with modelled snow depth above 50 cm on 15 February at this elevation", shown with its period and data type. Weightings for a combined score wait until inputs and limitations are documented.

Sources: [Open-Meteo historical API](https://open-meteo.com/en/docs/historical-weather-api), [Open-Meteo terms](https://open-meteo.com/en/terms), [Open-Meteo pricing](https://open-meteo.com/en/pricing), [SLF IMIS network](https://envidat.ch/dataset/imis-measuring-network), [Meteostat daily API](https://dev.meteostat.net/api/point/daily), [MeteoSwiss open data](https://opendatadocs.meteoswiss.ch/a-data-groundbased/a5-manual-precipitation-stations), [Météo-France avalanche bulletin XML](https://donneespubliques.meteofrance.fr/client/document/descriptif_bulletinrisqueavalanche_formatxml_20231026_309.pdf).
