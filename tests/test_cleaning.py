import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cleaning import clean_data  # noqa: E402


def make_df(**overrides):
    data = {
        "order_id": [1, 2, 3],
        "order_date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
        "sales": [100.0, 200.0, 300.0],
    }
    data.update(overrides)
    return pd.DataFrame(data)


def test_removes_exact_duplicates_and_reports_count():
    df = pd.concat([make_df(), make_df().iloc[[0]]], ignore_index=True)  # row 1 appears twice
    out, report = clean_data(df)
    assert len(out) == 3
    assert report["rows_in"] == 4
    assert report["duplicates"] == 1
    assert report["rows_out"] == 3


def test_drops_missing_and_non_positive_sales_and_report_adds_up():
    df = make_df(
        order_id=[1, 2, 3, 4, 5],
        order_date=pd.to_datetime(["2024-01-01", None, "2024-01-03", "2024-01-04", "2024-01-05"]),
        sales=[100.0, 50.0, "abc", 0, -25.0],
    )
    out, report = clean_data(df)
    # only row 1 is valid: row 2 has no date, row 3 sales is not a number,
    # row 4 is zero and row 5 is negative
    assert out["order_id"].tolist() == [1]
    assert report["missing"] == 2
    assert report["non_positive"] == 2
    assert report["rows_in"] - report["duplicates"] - report["missing"] - report["non_positive"] == report["rows_out"]
    assert pd.api.types.is_numeric_dtype(out["sales"])


def test_trims_text_keeps_numeric_ids_and_does_not_mutate_input():
    df = make_df(region=[" East ", "West", "South  "], customer_id=[101, "A-1 ", 303])
    snapshot = df.copy(deep=True)
    out, _ = clean_data(df)
    assert out["region"].tolist() == ["East", "West", "South"]
    assert out["customer_id"].tolist() == [101, "A-1", 303]  # numeric ids must not become NaN
    pd.testing.assert_frame_equal(df, snapshot)  # caller's dataframe is untouched
