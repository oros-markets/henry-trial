# Quantitative Research Work Trial: Rhodium Pricing

Develop the strongest model you can for rhodium price returns, with corresponding price forecasts in US dollars per pound (USD/lb), using the supplied data as your starting point.

The target is the **Johnson Matthey London daily rhodium Base Price**, using the supplied history from **January 1996 onward** in [johnson_matthey_rhodium_daily.parquet](data/johnson_matthey_rhodium_daily.parquet). Predict returns and report corresponding price forecasts in **USD per pound**.

Use `price_usd_per_lb`. The file also retains the original USD-per-troy-ounce quote; the conversion to a standard avoirdupois pound is `7000 / 480`. Percentage returns are unchanged by this conversion.

This is a deliberately open-ended research problem. You own the work from feature selection onward, including problem formulation, feature engineering, modeling, validation, and interpretation. Focus primarily on horizons of roughly 6–12 months. You may experiment with other horizons, but every prediction horizon must be at least 3 months. Define and justify your horizons, forecast frequency, and the information available at the time each prediction is made.

We are interested in both predictive performance and the quality of your research judgment. This is a difficult problem. Strong work explains what worked, what did not, and why.

## Data

The data lives in `data/`. [FEATURES_CATALOG.md](FEATURES_CATALOG.md) explains what each dataset measures, its source and coverage.

Check date alignment, missing observations, publication delays, revisions, and feature availability before modeling. Avoid data leakage: a reporting period is not necessarily the date its value became available. Document assumptions where historical release information is unavailable.

Use either starter notebook in `notebooks/` for exploration:

- `exploration.ipynb` — Jupyter notebook
- `exploration.py` — Marimo notebook

Install dependencies with `uv sync`, then open a notebook with `uv run jupyter lab` or `uv run marimo edit notebooks/exploration.py`.

## Research approach and evaluation

Choose the methods you believe are appropriate and explain your reasoning. There is no prescribed model family, feature set, or backtesting scheme. Creativity is welcome when supported by a clear hypothesis and credible evaluation.

Evaluate forecasts of the change in rhodium's price over each horizon. Use simple cumulative returns:

`r(t, h) = P(t + h) / P(t) - 1`

You may model log returns or price levels internally, but convert predictions to this basis for comparison. Explain how calendar horizons map to observed price dates.

Report out-of-sample results separately for each horizon, including:

- R² on rhodium price returns. State the definition and how results are aggregated across backtest folds.
- MAE of the corresponding price forecasts in USD/lb.
- RMSE of price forecasts, plus MAE and RMSE of returns. Label return errors clearly as decimal returns or percentage points.

Explain which objective guided model selection and how you weighed competing metrics. Compare with a zero-return forecast, equivalent to predicting that the future price equals the most recently available price, and any other useful baselines. “Returns” here means changes in the price of rhodium; a trading strategy is not required.

Choose and justify a backtesting scheme appropriate for time-dependent data. Document the training and evaluation periods, retraining schedule, and model-selection process. At each training cutoff, use only examples whose forward-return outcomes would already have been observed. Account for overlapping forecast horizons when designing splits and interpreting results. Clearly distinguish results used to guide development from any final held-out evaluation.

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
