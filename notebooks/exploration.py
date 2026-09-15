import marimo

__generated_with = "0.10.0"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    sns.set_theme()
    return Path, np, pd, plt, sns


@app.cell
def _(Path):
    root = Path.cwd()
    data_dir = (root if (root / "data").is_dir() else root.parent) / "data"
    files = sorted(data_dir.glob("*.parquet"))
    files
    return data_dir, files


if __name__ == "__main__":
    app.run()
