# Features Catalog

## Target and related metal prices

Use `rhodium_usd_per_troy_oz` in [jm_pgm_prices_daily.parquet](data/jm_pgm_prices_daily.parquet) as the target. The same table contains `platinum_usd_per_troy_oz`, `palladium_usd_per_troy_oz`, `iridium_usd_per_troy_oz`, and `ruthenium_usd_per_troy_oz`. Each row is one quoted date; all prices are Johnson Matthey New York quotes in **USD/troy oz**.

See [TRIAL.md](TRIAL.md) for the research task and evaluation requirements.

## Available datasets

Coverage lists the first and last observations. Individual series may start later or contain gaps. Original records and provenance are in [data/sources](data/sources/README.md) and the Parquet metadata.

| Dataset | Frequency | Coverage | Content and source |
| --- | --- | --- | --- |
| [Johnson Matthey PGM prices](data/jm_pgm_prices_daily.parquet) | Daily quotes | 1996-09-16 to 2026-09-15 | New York prices for rhodium, platinum, palladium, iridium, and ruthenium, all in USD/troy oz. Rhodium is the target. |
| [Alternative PGM quotes](data/pgm_alternative_quotes_daily.parquet) | Daily | 2018-01-01 to 2026-09-10 | Separate USD quotes for the same five metals, with open, high, low, and close fields. Prices differ from JM; the source does not specify the weight unit. |
| [China vehicle production](data/china_vehicle_production_monthly.parquet) | Monthly | 1995-02 to 2026-07 | Total motor vehicles produced in China. Source: ChinaData. |
| [China new-energy vehicle production](data/china_new_energy_vehicle_production_monthly.parquet) | Monthly | 2023-03 to 2026-07 | Vehicles produced in the source’s new-energy category. Source: ChinaData / NBS. |
| [South African total mining](data/sa_total_mining_production_monthly.parquet) | Monthly | 1975-01 to 2023-10 | Total mining output index, 2015 = 100, without seasonal adjustment. Source: FRED / OECD. |
| [EU electric cars](data/eu_electric_cars_annual.parquet) | Annual | 2010 to 2025 | Electric-car sales, fleet size, and market shares by powertrain. Source: IEA. |
| [US light vehicle sales](data/us_light_vehicle_sales_monthly.parquet) | Monthly | 1976-01 to 2026-08 | Car and light-truck sales in millions, at a seasonally adjusted annual rate. Source: FRED / ALTSALES. |
| [South African rhodium exports](data/sa_rhodium_exports_monthly.parquet) | Monthly | 2010-01 to 2026-05 | Export value, shipment weight, and USD/kg unit value for unwrought or powdered rhodium. Source: UN Comtrade. |
| [Rand / US dollar](data/usd_zar_exchange_rate_daily.parquet) | Weekdays | 1980-01-02 to 2026-09-11 | South African rand per US dollar; an increase means a weaker rand. Source: FRED / DEXSFUS. |
| [South African mining detail](data/sa_mining_production_sales_monthly.parquet) | Monthly | 1980-01 to 2026-07 | Production indices (2019 = 100) and sales in millions of rand by mineral, including PGMs. Source: Statistics South Africa / P2041. |
| [Rhodium supply and demand](data/jm_rhodium_supply_demand_annual.parquet) | Annual | 1985 to 2026 | Regional primary supply, recycling, demand by industry, and surplus or deficit, in thousands of ounces. Source: Johnson Matthey, May 2026. |
| [Platinum and palladium positions](data/cftc_pt_pd_open_interest.csv) | Weekly | 2006-06-13 to 2026-09-08 | Futures open interest and managed-money long and short positions, in contracts. Source: CFTC. |
| [Russia geopolitical risk](data/russia_geopolitical_risk_index.parquet) | Monthly | 1900-01 to 2026-08 | Share of newspaper articles about geopolitical risk involving Russia. The recent measure starts in 1985. Source: GPR workbook. |
| [China electric cars](data/iea_china_ev_sales.parquet) | Annual | 2010 to 2025 | Electric-car sales, fleet size, shares, battery deployment, electricity use, and estimated oil displacement. Source: IEA. |

## Timing notes

- JM quotes have longer gaps in January 2003, 2016, and 2017. They are not interpolated; use observed dates when mapping forecast horizons.
- The 2026 annual supply/demand figures are a May 2026 outlook. Account for publication timing and revisions when aligning features to forecasts.
- Export unit values use net weight, except July 2021 and February 2026, which use reported alternate kilogram quantities; `unit_value_weight_basis` identifies these rows.
