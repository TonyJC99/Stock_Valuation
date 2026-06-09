import pandas as pd


def load_statements(filepath: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Load raw file
    raw = pd.read_csv(filepath, encoding="latin-1", header=None)
    raw.columns = ["Category", "2025", "2024", "2023"]

    # Locate section boundaries
    def find_row(keyword: str) -> int:
        matches = raw.index[raw["Category"].str.strip() == keyword]
        if matches.empty:
            raise ValueError(f"Section header not found: '{keyword}'")
        return matches[0]

    income_header   = find_row("Consolidacion de los Estados de Resultados y Otros Resultados Integrales")
    cashflow_header = find_row("Estado Consolidado de Flujos de Efectivo")

    # Slice each section
    balance_df  = raw.iloc[1 : income_header].copy()
    income_df   = raw.iloc[income_header + 2 : cashflow_header].copy()
    cashflow_df = raw.iloc[cashflow_header + 2 :].copy()

    # Clean and cast numeric columns
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        df = df[df["Category"].notna()]
        df = df[df["Category"].str.strip() != ""]
        df = df.reset_index(drop=True)
        for col in ["2025", "2024", "2023"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    balance_df  = clean(balance_df)
    income_df   = clean(income_df)
    cashflow_df = clean(cashflow_df)

    return balance_df, income_df, cashflow_df


if __name__ == "__main__":
    bs, inc, cf = load_statements("Grupo_Melo_CFS.csv")

    for name, df in [("Balance Sheet", bs), ("Income Statement", inc), ("Cash Flow", cf)]:
        print(f"\n{name} ({len(df)} rows)")
        print(df.to_string(index=False))