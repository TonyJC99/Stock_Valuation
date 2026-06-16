# Grupo Melo Stock Valuation

Python valuation tool for Grupo Melo (Bolsa de Valores de Panamá). Combines ratio analysis with a DCF model to estimate intrinsic share value.

## What it does

Analyzes Grupo Melo's consolidated financial statements (2023-2025) and outputs:

- Profitability, leverage, and market ratios across three fiscal years
- A 5-year DCF valuation with intrinsic value per share
- A sensitivity table across discount rate and terminal growth assumptions

## Result

At a 10% discount rate and 3% terminal growth, the model gives an intrinsic value of $147.22/share against a market price of $54.80/share. The sensitivity table holds the same direction across all tested combinations (8-14% discount rate, 2-4% terminal growth).

A 2.7x gap between intrinsic and market value is large enough that the cash flow assumptions deserve scrutiny before treating this as a real signal. See Limitations.

## How it works

1. `load_data.py` parses the raw CSV (balance sheet, income statement, cash flow stacked in one file) and splits it into three DataFrames.
2. `valuation.py` loads those statements, calculates ratios (ROE, ROA, Net Margin, Debt/Equity, EPS, P/E, P/B), runs the DCF, builds the sensitivity table, and exports everything as CSVs for Power BI.

```
Grupo_Melo_CFS.csv → load_data.py → valuation.py → exports/*.csv → Power BI dashboard
```

## Ratios calculated

| Ratio | Formula |
|---|---|
| ROE | Net Income / Total Equity |
| ROA | Net Income / Total Assets |
| Net Margin | Net Income / Revenue |
| Debt/Equity | Total Liabilities / Total Equity |
| EPS | Net Income / Shares Outstanding |
| P/E | Price per Share / EPS |
| P/B | Market Cap / Total Equity |

## DCF assumptions

- Base year FCF: Operating Cash Flow + CapEx (2025)
- Projection period: 5 years
- Base case: 10% discount rate, 3% terminal growth
- Terminal value via Gordon Growth Model

## Limitations

- FCF growth is held constant at the terminal rate across all 5 projection years instead of declining or stepping down — this can overstate intrinsic value.
- Projections are based on a single year (2025) rather than a normalized multi-year average.
- No adjustment for one-time items in cash flow or net income.

## Stack

Python (pandas), Power BI

## Running it

```
pip install pandas
python valuation.py
```

Outputs three CSVs to `exports/`: `ratios.csv`, `dcf.csv`, `sensitivity.csv`. Import into Power BI to reproduce the dashboard.

## Author

Antonio J. Caballero de la Guardia
