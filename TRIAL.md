# Quantitative Research Work Trial: Rhodium Pricing

Develop a predictive model you can for rhodium price returns, with corresponding price forecasts in US dollars per troy ounce (USD/troy oz), using the supplied data as your starting point. You only need to build a forecasting model; a trading strategy is not required.

The target is the **Johnson Matthey New York daily rhodium Base Price**, using the supplied history from **16 September 1996 onward** in [jm_pgm_prices_daily.parquet](data/jm_pgm_prices_daily.parquet). Predict returns and report corresponding price forecasts in **USD/troy oz**.

Use `rhodium_usd_per_troy_oz` as the target price. The same table provides daily platinum, palladium, iridium, and ruthenium prices as candidate features. All five series use the source’s USD/troy oz quotes without unit conversion.

This is a deliberately open-ended research problem. You own the work from feature selection onward, including problem formulation, feature engineering, modeling, validation, and interpretation. Focus primarily on horizons of roughly 6–12 months. You may experiment with other horizons, but every prediction horizon must be at least 3 months. Define and justify your horizons, forecast frequency, and the information available at the time each prediction is made.

We are interested in both predictive performance and the quality of your research judgment. This is a difficult problem, so we're more interested in your thought process! Be sure to keep justifications for choices and methodology.

## Data

The data lives in `data/`. [FEATURES_CATALOG.md](FEATURES_CATALOG.md) explains what each dataset measures, its source and coverage.

Check date alignment, missing observations, publication delays, revisions, and feature availability before modeling. Avoid data leakage: a reporting period is not necessarily the date its value became available. Document assumptions where historical release information is unavailable.

Use either starter notebook in `notebooks/` for exploration:

- `exploration.ipynb` — Jupyter notebook
- `exploration.py` — Marimo notebook

Install dependencies with `uv sync`, then open a notebook with `uv run jupyter lab` or `uv run marimo edit notebooks/exploration.py`.

## Research approach and evaluation

Choose the methods you believe are appropriate and explain your reasoning. There is no prescribed model family, feature set, or backtesting schema. Creativity is welcome when supported by a clear hypothesis and credible evaluation.

Evaluate forecasts of the change in rhodium's price over each horizon. Use simple cumulative returns:

`r(t, h) = P(t + h) / P(t) - 1`

You may model log returns or price levels internally, but convert predictions to this basis for comparison. Explain how calendar horizons map to observed price dates.

Report out-of-sample results separately for each horizon, including (you're not limited to this):

- R² on rhodium price returns.
- MAE of the corresponding price forecasts in USD/troy oz.
- RMSE of price forecasts, plus MAE and RMSE of returns. Label return errors clearly as decimal returns or percentage points.

Explain which objective guided model selection and how you weighed competing metrics. Choose and justify a backtesting schema appropriate for time-dependent data. Document the training and evaluation periods, retraining schedule, and model-selection process. Clearly distinguish results used to guide development from any final evaluation.

## Additional data

The supplied features are a starting point. You may research alternative features or data sources if you believe they would improve the model or test a useful hypothesis.

If you would like us to collect additional data, tell us:

- What feature or source you propose, with a link where available.
- Why it may be useful and what hypothesis it would help test.
- The historical coverage, frequency, and fields you need.
- Any known publication delays or access constraints.

We can help scrape or obtain relevant records, subject to availability. Document how additional data contributes to your approach.

## Deliverable

Submit a report that covers:

1. **Problem formulation:** Your interpretation of the task, prediction horizon, and key assumptions.
2. **Selected model:** The approach you settled on, why you chose it, and alternatives considered.
3. **Features:** Selected features and transformations, their rationale, and how you handled timing and availability.
4. **Backtesting and performance:** Evaluation scheme, baseline comparisons, and out-of-sample return and price metrics for each horizon.
5. **Research process:** Main hypotheses, experiments, unsuccessful approaches, and findings that informed your decisions.
6. **Limitations and next steps:** Where the approach is weakest, what remains uncertain, and what you would investigate with more time or data.

The report should make the research process understandable, not just present final results. Focus on the decisions and evidence that shaped your conclusions; an exhaustive diary of every experiment is unnecessary.
