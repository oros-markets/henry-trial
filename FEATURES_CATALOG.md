# Features Catalog

## Target

[Johnson Matthey London daily rhodium](data/johnson_matthey_rhodium_daily.parquet): **January 1996–September 2026**, on quoted dates. Use `price_usd_per_lb` for prices and derive forward returns as described in the [trial brief](TRIAL_README.md). Original quotes are retained in `price_usd_per_troy_oz`. [Source: Johnson Matthey](https://matthey.com/en/products-and-markets/pgms-and-circularity/pgm-management).

## Candidate features

Coverage shows the first and last available records; individual series may start later or contain gaps. Source records are preserved in [data/sources](data/sources/README.md) or the supplied Parquet metadata.

| Dataset | Frequency · coverage | What it measures | Source |
| --- | --- | --- | --- |
| [PGM prices](data/bds_5529cd6bc41841d7b58fb69e90cd2546__pgm_price_history.parquet) | Daily · 2018-01–2026-09 | USD quotes for platinum, palladium, rhodium, ruthenium, and iridium; includes open, high, low, and close fields. | Supplied price-history feed |
| [China vehicle production](data/bds_59f19703af7c45bab999c0ed86851136__chinadata_vehicle_production.parquet) | Monthly · 1995-02–2026-07 | Total motor vehicles produced in China. | ChinaData |
| [China new-energy vehicle production](data/bds_06c4bc4f03a645bf951a92f8e59c3006__chinadata_ev_production.parquet) | Monthly · 2023-03–2026-07 | Output of vehicles classified by the source as new-energy vehicles. | ChinaData / NBS |
| [South African mining](data/bds_68ec2edb578d4f93af8bc60fc0db9777__fred_zafprmito01ixobm_history.parquet) | Monthly · 1975-01–2023-10 | Total mining output index, 2015 = 100, without seasonal adjustment. | FRED / OECD |
| [EU electric cars](data/bds_8a05db43d9ba4fe58ec076250a56f1f9__iea_evs_eu_cars_historical.parquet) | Annual · 2010–2025 | Electric-car sales, fleet size, and market shares by powertrain. | IEA |
| [US vehicle sales](data/bds_92934197439c46fc9622dfc440cace8f__fred_altsales_history.parquet) | Monthly · 1976-01–2026-08 | Car and light-truck sales in millions, at a seasonally adjusted annual rate. | FRED / ALTSALES |
| [South African rhodium exports](data/bds_fb39b19cbcc4464abc5ca4dbbdf4cf1f__un_comtrade_sa_refined_rhodium_monthly.parquet) | Monthly · 2010-01–2026-05 | Export value, shipment weight, and USD/kg unit value for unwrought or powdered rhodium. | UN Comtrade |
| [Rand / dollar](data/bds_fed88706ea3046d4a66c7c7c7c71ef12__fred_dexsfus_history.parquet) | Weekdays · 1980-01–2026-09 | South African rand per US dollar; an increase means a weaker rand. | FRED / DEXSFUS |
| [South African mining detail](data/sa_mining_production_sales_monthly.parquet) | Monthly · 1980-01–2026-07 | Production indices (2019 = 100) and sales in millions of rand by mineral, including PGMs. | Statistics South Africa / P2041 |
| [Rhodium supply and demand](data/jm_rhodium_supply_demand_annual.parquet) | Annual · 1985–2026 | Regional primary supply, recycling, demand by industry, and surplus or deficit, in thousands of ounces. | Johnson Matthey, May 2026 |
| [Platinum and palladium positions](data/cftc_pt_pd_open_interest.csv) | Weekly · 2006-06–2026-09 | Futures open interest and managed-money long and short positions, in contracts. | CFTC |
| [Russia geopolitical risk](data/russia_geopolitical_risk_index.parquet) | Monthly · 1900-01–2026-08 | Share of newspaper articles about geopolitical risk involving Russia; recent measure starts in 1985. | GPR source workbook |
| [China electric cars](data/iea_china_ev_sales.parquet) | Annual · 2010–2025 | Electric-car sales, fleet size, shares, battery deployment, electricity use, and estimated oil displacement. | IEA |

**Usage notes:** Annual 2026 supply/demand figures are a May 2026 outlook. Keep battery-electric, plug-in hybrid, and fuel-cell vehicles separate. Trade unit values use net weight, with reported alternate kilogram quantities for July 2021 and February 2026 (`unit_value_weight_basis`). Account for publication timing and revisions when aligning features to forecasts.
