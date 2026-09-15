# Attached source files

This directory holds original attachments and downloaded source records. The [import manifest](import_manifest.json) records each original filename and SHA-256 hash.

| Preserved source | Research table |
| --- | --- |
| `sa_mining_1980_2002.xlsx` and `sa_mining_2003_onward.xlsx` | [Merged monthly mining production and sales](../sa_mining_production_sales_monthly.parquet) |
| `jm_rhodium_supply_demand_may_2026.xlsx` | [Annual rhodium supply and demand](../jm_rhodium_supply_demand_annual.parquet) |
| `russia_geopolitical_risk_index.xls` | [Russia geopolitical risk](../russia_geopolitical_risk_index.parquet) |
| `iea_china_ev_sales.csv` | [China EV sales and related historical measures](../iea_china_ev_sales.parquet) |

The CFTC attachment is preserved directly as [cftc_pt_pd_open_interest.csv](../cftc_pt_pd_open_interest.csv), renamed from `72hh-3qpy (1).csv`. Read `cftc_contract_market_code` as text to preserve leading zeros.

The renamed Russia risk workbook retains all original countries, global indices, and variable labels. The cleaned research table selects `month`, `GPRC_RUS`, and `GPRHC_RUS`, with `month` represented as `period` (`YYYY-MM`). The two Russia measures remain separate.

## Rebuild the research tables

From the repository root:

```sh
uv run --extra data-import python scripts/import_trial_attachments.py
```

The import uses the preserved attachments, requires no network data access, and does not modify the separately supplied monthly and daily datasets. It checks source-series metadata compatibility, unique keys, source row counts, continuous monthly coverage, annual supply/demand identities, and Parquet round-trip equality. It retains missing values and does not fill absent series history.

See the [Features Catalog](../../FEATURES_CATALOG.md) for dataset descriptions.

## Daily rhodium target and trade records

`jm_pgm_new_york_daily.csv` is the unmodified Johnson Matthey New York export downloaded on 15 September 2026. It contains five metals; the research table retains every observation for all five metals, with rhodium as the prediction target, from 16 September 1996 to 15 September 2026. Prices are USD per troy ounce. No start-date filter or interpolation is applied. See [source provenance](target_provenance.json).

`un_comtrade_original.parquet` preserves the supplied trade data before restoring two unit values. `comtrade_202107.json` and `comtrade_202602.json` contain the source responses with alternate quantities in kilograms (unit code 8). The original net weights remain unchanged. `comtrade_202012.json` records an empty response for December 2020.

Rebuild the target and restored trade values without network access:

```sh
uv run python scripts/prepare_target.py
```

## Heraeus Precious Metals prices

[pgm_alternative_quotes_daily.parquet](../pgm_alternative_quotes_daily.parquet) contains Heraeus Precious Metals quotes for platinum, palladium, rhodium, iridium, and ruthenium. Heraeus and Johnson Matthey are separate dealers with different price discovery. The Heraeus dataset is retained for its additional open, high, low, and close (OHLC) fields, particularly for platinum and palladium. The recorded price-history endpoint is preserved in the Parquet metadata. Currency is recorded as USD; the weight unit is not specified in that metadata.

## Crucible futures

The local futures files were retrieved from Crucible’s `market_resampled_bars` dataset on 15 September 2026. The source is CME Group via Databento. The [manifest](crucible_futures_manifest.json) records the exact series IDs, source handles, units, checksums, coverage, and longer gaps.

| File | Contract | Rows | Available dates | Price unit |
| --- | --- | --- | --- | --- |
| [aluminum_futures_daily.parquet](../aluminum_futures_daily.parquet) | COMEX aluminum, ALI, front continuous | 1,306 | 2014-05-06 to 2026-06-19 | USD/metric tonne |
| [copper_futures_daily.parquet](../copper_futures_daily.parquet) | COMEX copper, HG, front continuous | 4,502 | 2010-06-07 to 2026-06-28 | USD/lb |

Each row contains `observation_date`, UTC `bar_start_time` and `bar_end_time`, `open`, `high`, `low`, `close`, and `volume`, plus source and revision fields. Volume is in contracts. Prices retain the source units. These are daily OHLCV bars, not official settlements. The continuous series use unadjusted days-before-expiry rolls; the source does not supply the exact roll-day count. Contract changes can create price jumps.

`observation_date` is the UTC bar-start date. A completed bar is available no earlier than `bar_end_time`. `revision_observed_at` records a Crucible revision timestamp, not the original market publication time. No dates or prices have been interpolated. Aluminum is sparse, with a largest interval between observations of 672 calendar days; copper’s largest interval is five days. The source’s `completeness_state` describes individual bars, not completeness of the history.

Both files have unique dates, non-null OHLCV fields, nonnegative volume, and consistent OHLC ranges. All returned observations were retained and checked after saving. The extraction queried 2010 onward; dates above describe the returned records. The source snapshots stop in June 2026.

Contract references: [CME aluminum](https://www.cmegroup.com/markets/metals/base/aluminum.contractSpecs.html) and [CME copper](https://www.cmegroup.com/markets/metals/base/copper.html).
