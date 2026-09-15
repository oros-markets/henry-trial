"""Prepare the full New York target and source-backed trade unit values offline."""
from pathlib import Path
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data/sources"
prices = pd.read_csv(SOURCES / "jm_pgm_new_york_daily.csv", skiprows=1)
prices["observation_date"] = pd.to_datetime(prices.Date, format="%d-%b-%Y")
prices = prices.sort_values("observation_date")
metals = ["Platinum", "Palladium", "Rhodium", "Iridium", "Ruthenium"]
price_columns = {metal: f"{metal.lower()}_usd_per_troy_oz" for metal in metals}
target = prices[["observation_date", *metals]].rename(columns=price_columns).reset_index(drop=True)
target["quote_region"] = "New York"
assert target.observation_date.is_unique and target.notna().all().all()
assert target[list(price_columns.values())].gt(0).all().all()
target.to_parquet(ROOT / "data/jm_pgm_prices_daily.parquet", index=False)
original = pq.read_table(SOURCES / "un_comtrade_original.parquet")
trade = original.to_pandas()
trade["alternate_quantity_kg"] = float("nan")
trade["unit_value_weight_basis"] = "net_weight_kg"
for period in ["202107", "202602"]:
    receipt = json.loads((SOURCES / f"comtrade_{period}.json").read_text())
    rows = receipt["data"]
    assert len(rows) == 1
    row = rows[0]
    assert row["altQtyUnitCode"] == 8 and row["altQty"] > 0
    mask = trade.period.astype(str).eq(period)
    assert mask.sum() == 1 and trade.loc[mask, "unit_value_usd_per_kg"].isna().all()
    assert abs(trade.loc[mask, "primary_value_usd"].iloc[0] - row["primaryValue"]) < 0.01
    trade.loc[mask, "alternate_quantity_kg"] = row["altQty"]
    trade.loc[mask, "unit_value_usd_per_kg"] = row["primaryValue"] / row["altQty"]
    trade.loc[mask, "unit_value_weight_basis"] = "alternate_quantity_kg"
assert trade.unit_value_usd_per_kg.notna().all()
out = pa.Table.from_pandas(trade, preserve_index=False)
# Preserve the supplied scrape provenance alongside the new columns.
metadata = dict(original.schema.metadata or {})
metadata.update(out.schema.metadata or {})
out = out.replace_schema_metadata(metadata)
pq.write_table(out, ROOT / "data/sa_rhodium_exports_monthly.parquet")
print(f"Target: {len(target):,} observations, {target.observation_date.min().date()} to {target.observation_date.max().date()}; two trade unit values restored.")
