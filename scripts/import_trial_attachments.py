"""Rebuild the additional research tables from the preserved user attachments.

Run from any directory: uv run --extra data-import python scripts/import_trial_attachments.py
The separately supplied monthly and daily datasets are not changed by this script.
"""

from pathlib import Path
import hashlib
import json
import re

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SOURCES = DATA / "sources"


def save_table(frame, name, key):
    frame = frame.copy()
    for column in frame.select_dtypes("object"):
        frame[column] = frame[column].astype("string")
    assert not frame.duplicated(key).any(), f"Duplicate key in {name}"
    assert not np.isinf(frame.select_dtypes("number")).any().any()
    path = DATA / name
    frame.to_parquet(path, index=False)
    pd.testing.assert_frame_equal(frame, pd.read_parquet(path))
    return {"file": name, "rows": len(frame), "columns": len(frame.columns),
            "key": key, "null_counts": frame.isna().sum().to_dict()}


def merge_mining():
    mapping = {
        "H01": "publication_code", "H02": "publication_name", "H03": "series_id",
        "H04": "measure", "H05": "mineral_group", "H06": "mineral_detail",
        "H16": "adjustment", "H17": "unit", "H18": "base_period", "H25": "frequency",
    }
    parts, metadata = [], []
    for name in ["sa_mining_1980_2002.xlsx", "sa_mining_2003_onward.xlsx"]:
        book = pd.ExcelFile(SOURCES / name)
        frame = pd.read_excel(book, sheet_name=0)
        months = [c for c in frame if re.fullmatch(r"MO\d{6}", str(c))]
        assert set(frame.columns) == set(mapping) | set(months)
        assert not frame.H03.duplicated().any()
        metadata.append(frame[list(mapping)].set_index("H03").sort_index())
        frame["source_excel_row"] = np.arange(2, len(frame) + 2)
        tidy = frame.melt(id_vars=list(mapping) + ["source_excel_row"],
                          value_vars=months, var_name="source_period_column", value_name="value")
        tidy["period"] = pd.to_datetime(tidy.source_period_column, format="MO%m%Y").dt.strftime("%Y-%m")
        tidy["value"] = pd.to_numeric(tidy.value, errors="raise").astype(float)
        assert tidy.value.notna().all()
        tidy["source_file"] = name
        tidy["source_sheet"] = book.sheet_names[0]
        parts.append(tidy.rename(columns=mapping))
    shared = metadata[0].index.intersection(metadata[1].index)
    pd.testing.assert_frame_equal(metadata[0].loc[shared], metadata[1].loc[shared])
    result = pd.concat(parts, ignore_index=True).sort_values(["series_id", "period"]).reset_index(drop=True)
    assert len(result) == 41 * 276 + 42 * 283
    for _, group in result.groupby("series_id"):
        dates = pd.to_datetime(group.period)
        assert len(pd.date_range(dates.min(), dates.max(), freq="MS")) == len(group)
    columns = ["period", "series_id", "value"] + [c for c in result if c not in ["period", "series_id", "value"]]
    return result[columns]


def rhodium_supply_demand():
    name = "jm_rhodium_supply_demand_may_2026.xlsx"
    raw = pd.read_excel(SOURCES / name, sheet_name="Rhodium", header=None)
    row_sections = {**dict.fromkeys(range(5, 11), "primary_supply"),
                    13: "secondary_supply", 14: "secondary_supply", 16: "combined_supply",
                    **dict.fromkeys(range(19, 25), "demand"), 26: "market_balance"}
    records = []
    for row, section in row_sections.items():
        for column in range(1, raw.shape[1]):
            year = int(raw.iloc[3, column])
            records.append({"year": year, "section": section, "series_name": raw.iloc[row, 0],
                            "value": raw.iloc[row, column], "unit": raw.iloc[3, 0],
                            "report_vintage": "2026-05", "is_report_year": year == 2026,
                            "source_file": name, "source_sheet": "Rhodium",
                            "source_excel_row": row + 1, "source_excel_column": column + 1})
    result = pd.DataFrame(records).sort_values(["section", "series_name", "year"]).reset_index(drop=True)
    result["value"] = pd.to_numeric(result.value, errors="raise").astype(float)
    assert len(result) == 16 * 42
    assert result.value.isna().sum() == 15  # Zimbabwe, 1985–1999: preserve blank observations.
    totals = result.pivot(index="year", columns="series_name", values="value")
    np.testing.assert_allclose(totals["Total combined supply"], totals["Total Supply"] + totals["Total secondary supply"])
    np.testing.assert_allclose(totals["Movements in Stocks"], totals["Total combined supply"] - totals["Total Demand"])
    return result


def russia_risk():
    raw = pd.read_excel(SOURCES / "russia_geopolitical_risk_index.xls")
    result = raw[["month", "GPRC_RUS", "GPRHC_RUS"]].copy()
    result.insert(0, "period", pd.to_datetime(result.pop("month")).dt.strftime("%Y-%m"))
    assert len(result) == 1520
    assert result.GPRC_RUS.isna().sum() == 1020
    assert result.GPRHC_RUS.notna().all()
    labels = dict(raw[["var_name", "var_label"]].dropna().itertuples(index=False, name=None))
    assert "Percent of articles (Russia)" in labels["GPRC_RUS"]
    return result


def main():
    profiles = [
        save_table(merge_mining(), "sa_mining_production_sales_monthly.parquet", ["period", "series_id"]),
        save_table(rhodium_supply_demand(), "jm_rhodium_supply_demand_annual.parquet", ["year", "section", "series_name"]),
        save_table(russia_risk(), "russia_geopolitical_risk_index.parquet", ["period"]),
    ]
    china = pd.read_csv(SOURCES / "iea_china_ev_sales.csv")
    assert china.region.eq("China").all() and china.category.eq("Historical").all() and china["mode"].eq("Cars").all()
    profiles.append(save_table(china, "iea_china_ev_sales.parquet",
                               ["region", "category", "parameter", "mode", "powertrain", "year", "unit"]))
    cftc = pd.read_csv(DATA / "cftc_pt_pd_open_interest.csv", dtype={"cftc_contract_market_code": str})
    assert set(cftc.cftc_contract_market_code) == {"075651", "076651"}
    assert not cftc.duplicated(["report_date_as_yyyy_mm_dd", "cftc_contract_market_code"]).any()
    assert not cftc.isna().any().any()
    profiles.append({"file": "cftc_pt_pd_open_interest.csv", "rows": len(cftc), "columns": len(cftc.columns)})
    source_names = {
        "sources/sa_mining_1980_2002.xlsx": "Excel table for 1980-2002.xlsx",
        "sources/sa_mining_2003_onward.xlsx": "Excel table from 2003.xlsx",
        "sources/jm_rhodium_supply_demand_may_2026.xlsx": "PGM supply demand history May 2026 Rhodium (2).xlsx",
        "sources/russia_geopolitical_risk_index.xls": "data_gpr_export.xls",
        "sources/iea_china_ev_sales.csv": "IEA-EV-dataHistoricalCarsChina.csv",
        "cftc_pt_pd_open_interest.csv": "72hh-3qpy (1).csv",
    }
    receipt = {"sources": [{"file": name, "original_filename": original,
                            "sha256": hashlib.sha256((DATA / name).read_bytes()).hexdigest()}
                           for name, original in source_names.items()], "outputs": profiles}
    (SOURCES / "import_manifest.json").write_text(json.dumps(receipt, indent=2) + "\n")
    for profile in profiles:
        print(f"{profile['file']}: {profile['rows']:,} rows, {profile['columns']} columns")


if __name__ == "__main__":
    main()
