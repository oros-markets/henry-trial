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

## Crucible market data

These files were retrieved through Crucible on 15 September 2026. Exact dataset IDs, snapshots, units, and checksums are in the [metals manifest](crucible_futures_manifest.json) and [energy/FX manifest](crucible_energy_fx_manifest.json).

| File | Source | Contents |
| --- | --- | --- |
| [aluminum_futures_daily.parquet](../aluminum_futures_daily.parquet) | CME / Databento | ALI front continuous contract; OHLC in USD/metric tonne and volume in contracts. |
| [copper_futures_daily.parquet](../copper_futures_daily.parquet) | CME / Databento | HG front continuous contract; OHLC in USD/lb and volume in contracts. |
| [wti_futures_curve_daily.parquet](../wti_futures_curve_daily.parquet) | CME / Databento | CL continuous contract ranks 1–12; OHLC in USD/barrel and volume in contracts. |
| [brent_futures_curve_daily.parquet](../brent_futures_curve_daily.parquet) | CME / Databento | BZ Brent Last Day Financial ranks 1–12; OHLC in USD/barrel and volume in contracts. |
| [usd_cny_exchange_rate_daily.parquet](../usd_cny_exchange_rate_daily.parquet) | FRED / DEXCHUS | `value` is yuan per US dollar; `vintage` identifies the source snapshot. |

For oil curves, one row is a `price_date` and `contract_rank`; rank 1 is the front contract, followed by successive contract positions. `contract_symbol` identifies a rolling series rather than a fixed delivery month. Futures prices are unadjusted OHLCV observations, not official settlements. Metals bars use UTC timestamps; use `bar_end_time` for completed-bar availability. Revision and vintage fields describe source snapshots, not historical release times.

Some observations are missing and coverage varies by rank; the files preserve those gaps. Detailed counts remain in the manifests.

Source references: [CME aluminum](https://www.cmegroup.com/markets/metals/base/aluminum.contractSpecs.html), [CME copper](https://www.cmegroup.com/markets/metals/base/copper.html), [CME WTI](https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.contractSpecs.html), [CME Brent](https://www.cmegroup.com/markets/energy/crude-oil/brent-crude-oil-last-day.contractSpecs.html), and [FRED DEXCHUS](https://fred.stlouisfed.org/series/DEXCHUS).
