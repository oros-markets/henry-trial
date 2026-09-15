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

The import uses the preserved attachments, requires no network data access, and does not modify the eight `bds_*` files. It checks source-series metadata compatibility, unique keys, source row counts, continuous monthly coverage, annual supply/demand identities, and Parquet round-trip equality. It retains missing values and does not fill absent series history.

See the [Features Catalog](../../FEATURES_CATALOG.md) for dataset descriptions.

## Daily rhodium target and trade records

`jm_rhodium_new_york_daily.csv` is the unmodified Johnson Matthey New York export downloaded on 15 September 2026. It contains five metals; the target selects every rhodium observation, from 16 September 1996 to 15 September 2026. Prices are USD per troy ounce. No start-date filter or interpolation is applied. See [source provenance](target_provenance.json).

`un_comtrade_original.parquet` preserves the supplied trade data before restoring two unit values. `comtrade_202107.json` and `comtrade_202602.json` contain the source responses with alternate quantities in kilograms (unit code 8). The original net weights remain unchanged. `comtrade_202012.json` records an empty response for December 2020.

Rebuild the target and restored trade values without network access:

```sh
uv run python scripts/prepare_target.py
```
