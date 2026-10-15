"""Data-cleaning step used by the dashboard (pandas only, no Streamlit)."""
import pandas as pd


def clean_data(df):
    """Removes duplicates, missing and invalid rows, and tidies text columns.
    Returns the cleaned dataframe and a report of what was removed."""
    report = {"rows_in": len(df)}
    df = df.copy()

    # 1. Duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates"] = before - len(df)

    # 2. Make sales numeric, then drop rows missing sales or date
    if "sales" in df.columns:
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    required = [c for c in ("sales", "order_date") if c in df.columns]
    before = len(df)
    if required:
        df = df.dropna(subset=required)
    report["missing"] = before - len(df)

    # 3. Drop zero or negative sales (returns, cancellations, bad entries)
    before = len(df)
    if "sales" in df.columns:
        df = df[df["sales"] > 0]
    report["non_positive"] = before - len(df)

    # 4. Trim stray spaces in text columns
    for c in ("region", "category", "product_name", "customer_id"):
        if c in df.columns and (pd.api.types.is_object_dtype(df[c]) or pd.api.types.is_string_dtype(df[c])):
            df[c] = df[c].str.strip().fillna(df[c])  # keep non-text values (e.g. numeric IDs) intact

    report["rows_out"] = len(df)
    return df, report
