"""Convert the Online Retail II CSV into the column layout the dashboard expects.

Usage:
    python scripts/prepare_retail_data.py "path/to/online_retail_II.csv" "path/to/retail_raw_1M.csv"

Only computes sales (Quantity x Price) and renames columns. It deliberately does NOT
remove duplicates, returns or missing values: the dashboard's own cleaning step does that.
Output is meant for local testing, so do not commit it (it is ~100 MB).
"""
import sys
import time
import pandas as pd


def main(src, dst):
    t = time.perf_counter()
    raw = pd.read_csv(src, encoding="latin1")
    print(f"Rows read: {len(raw):,}  ({time.perf_counter() - t:.2f}s)")

    df = pd.DataFrame({
        "order_id": raw["Invoice"],
        "order_date": raw["InvoiceDate"],
        "customer_id": raw["Customer ID"],
        "region": raw["Country"],
        "product_name": raw["Description"],
        # The dataset has no product category, so country is reused for the category chart
        "category": raw["Country"],
        "sales": raw["Quantity"] * raw["Price"],
    })
    df.to_csv(dst, index=False)
    print(f"Saved {len(df):,} rows to {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])