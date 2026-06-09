import pandas as pd
from load_data import load_statements

# Constants
SHARES_OUTSTANDING = 2_354_798
PRICE_PER_SHARE    = 54.80
DISCOUNT_RATE      = 0.10
TERMINAL_GROWTH    = 0.03
PROJECTION_YEARS   = 5

YEARS = ["2025", "2024", "2023"]

# Load statements
balance_df, income_df, cashflow_df = load_statements("Grupo_Melo_CFS.csv")

# Helper
def get(df, metric, year):
    row = df[df["Category"].str.strip() == metric]
    if row.empty:
        return None
    return pd.to_numeric(row[year].values[0], errors="coerce")


# Ratio analysis
ratios = []

for year in YEARS:
    total_assets = get(balance_df,  "Total de activos", year)
    total_equity = get(balance_df,  "Total de patrimonio", year)
    total_liab   = get(balance_df,  "Total de pasivos", year)
    net_income   = get(income_df,   "Utilidad (perdida) neta", year)
    revenue      = get(income_df,   "Ingresos de actividades ordinarias", year)

    eps          = net_income / SHARES_OUTSTANDING
    market_cap   = PRICE_PER_SHARE * SHARES_OUTSTANDING

    ratios.append({
        "Year":          year,
        "Revenue":       revenue,
        "Net Income":    net_income,
        "Total Assets":  total_assets,
        "Total Equity":  total_equity,
        "EPS":           eps,
        "ROE (%)":       net_income / total_equity * 100,
        "ROA (%)":       net_income / total_assets * 100,
        "Net Margin (%)": net_income / revenue * 100,
        "Debt/Equity":   total_liab / total_equity,
        "P/E Ratio":     PRICE_PER_SHARE / eps,
        "P/B Ratio":     market_cap / total_equity,
    })

ratios_df = pd.DataFrame(ratios)

print("RATIO ANALYSIS")
print(ratios_df.to_string(index=False))


# DCF valuation
op_cashflow = get(cashflow_df, "Efectivo neto de actividades de operación", "2025")
capex       = get(cashflow_df, "Adquisición de propiedades, mobiliario y equipo", "2025")
fcf         = op_cashflow + capex

projected_fcf = [fcf * (1 + TERMINAL_GROWTH) ** i for i in range(1, PROJECTION_YEARS + 1)]
pv_fcfs       = [v / (1 + DISCOUNT_RATE) ** i for i, v in enumerate(projected_fcf, 1)]

terminal_value   = projected_fcf[-1] * (1 + TERMINAL_GROWTH) / (DISCOUNT_RATE - TERMINAL_GROWTH)
pv_terminal      = terminal_value / (1 + DISCOUNT_RATE) ** PROJECTION_YEARS
enterprise_value = sum(pv_fcfs) + pv_terminal
intrinsic_value  = enterprise_value / SHARES_OUTSTANDING

print("\nDCF VALUATION")
print(f"  Free Cash Flow:        ${fcf:>12,.0f}")
print(f"  Enterprise Value:      ${enterprise_value:>12,.0f}")
print(f"  Intrinsic Value/Share: ${intrinsic_value:>10.2f}")
print(f"  Market Price:          ${PRICE_PER_SHARE:>10.2f}")

if intrinsic_value > PRICE_PER_SHARE:
    print(f"  VERDICT: UNDERVALUED by ${intrinsic_value - PRICE_PER_SHARE:.2f}")
else:
    print(f"  VERDICT: OVERVALUED by ${PRICE_PER_SHARE - intrinsic_value:.2f}")


# Sensitivity Analysis
sensitivity_rows = []

for dr in [0.08, 0.10, 0.12, 0.14]:
    for tg in [0.02, 0.03, 0.04]:
        pf  = [fcf * (1 + tg) ** i for i in range(1, PROJECTION_YEARS + 1)]
        pv  = [v / (1 + dr) ** i for i, v in enumerate(pf, 1)]
        tv  = pf[-1] * (1 + tg) / (dr - tg)
        ptv = tv / (1 + dr) ** PROJECTION_YEARS
        iv  = (sum(pv) + ptv) / SHARES_OUTSTANDING
        sensitivity_rows.append({
            "Discount Rate (%)": dr * 100,
            "Terminal Growth (%)": tg * 100,
            "Intrinsic Value": round(iv, 2),
        })

sensitivity_df = pd.DataFrame(sensitivity_rows)

print("\nSENSITIVITY ANALYSIS")
print(sensitivity_df.to_string(index=False))


# Export CSV for Power BI
import os
os.makedirs("exports", exist_ok=True)

ratios_df.to_csv("exports/ratios.csv", index=False)
sensitivity_df.to_csv("exports/sensitivity.csv", index=False)

dcf_df = pd.DataFrame([{
    "Free Cash Flow":        fcf,
    "Enterprise Value":      enterprise_value,
    "Intrinsic Value/Share": intrinsic_value,
    "Market Price":          PRICE_PER_SHARE,
    "Discount Rate (%)":     DISCOUNT_RATE * 100,
    "Terminal Growth (%)":   TERMINAL_GROWTH * 100,
}])
dcf_df.to_csv("exports/dcf.csv", index=False)

print("\nExports written to exports/")