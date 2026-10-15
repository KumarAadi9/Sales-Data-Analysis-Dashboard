"""Data-grounded chat for the sales dashboard.

Instead of sending summary stats and guessing, Gemini is given a tool
(`query_sales`) that runs real aggregations on the DataFrame. The model picks
the parameters, the code computes the exact numbers, and the model explains
them. No model-written code is ever executed.
"""
import pandas as pd

TIME_GROUPS = {"day": "D", "week": "W", "month": "M", "quarter": "Q", "year": "Y"}
AGGS = {"sum", "mean", "median", "max", "min", "count", "nunique"}
MAX_ROWS = 25


def _value_columns(df):
    return [c for c in ("sales", "profit", "quantity") if c in df.columns]


def build_schema_text(df):
    """Compact, factual description of the data so the model knows what exists."""
    lines = [f"Rows: {len(df):,}", f"Columns: {', '.join(df.columns)}"]
    if "order_date" in df.columns and df["order_date"].notna().any():
        lines.append(f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")
    for c in ("region", "category"):
        if c in df.columns:
            vals = df[c].dropna().unique()
            if len(vals) <= 20:
                lines.append(f"{c} values: {', '.join(map(str, vals))}")
            else:
                lines.append(f"{c}: {len(vals)} distinct values")
    return "\n".join(lines)


def execute_query(df, metric="sales", agg="sum", group_by="", region="", category="",
                  start_date="", end_date="", top_n=10, ascending=False):
    """Run a safe aggregation. Returns (result_text, dataframe_or_None)."""
    d = df
    try:
        if region and "region" in d.columns:
            d = d[d["region"].astype(str).str.lower() == region.lower()]
        if category and "category" in d.columns:
            d = d[d["category"].astype(str).str.lower() == category.lower()]
        if "order_date" in d.columns:
            if start_date:
                d = d[d["order_date"] >= pd.to_datetime(start_date)]
            if end_date:
                d = d[d["order_date"] <= pd.to_datetime(end_date)]
    except Exception as e:
        return f"Invalid filter: {e}", None

    if d.empty:
        return "No rows match those filters.", None

    agg = agg.lower()
    if agg not in AGGS:
        return f"agg must be one of {sorted(AGGS)}", None

    # Resolve the metric to a column / operation
    metric = metric.lower()
    if metric in ("orders", "order_count"):
        col, agg_eff = ("order_id", "nunique") if "order_id" in d.columns else (d.columns[0], "count")
    elif metric in ("customers", "customer_count"):
        if "customer_id" not in d.columns:
            return "This dataset has no customer_id column.", None
        col, agg_eff = "customer_id", "nunique"
    elif metric in d.columns and metric in _value_columns(d):
        col, agg_eff = metric, agg
    else:
        return f"Unknown metric '{metric}'. Use one of {_value_columns(d) + ['orders', 'customers']}.", None

    g = group_by.lower() if group_by else ""
    try:
        if not g:
            val = getattr(d[col], agg_eff)()
            return f"{agg_eff}({col}) = {val:,.2f}  (over {len(d):,} rows)", None
        if g in TIME_GROUPS:
            if "order_date" not in d.columns:
                return "No order_date column to group by time.", None
            per = d["order_date"].dt.to_period(TIME_GROUPS[g]).astype(str)
            res = d.groupby(per)[col].agg(agg_eff).sort_index()
            out = res.reset_index()
            out.columns = [g, f"{agg_eff}_{col}"]
            out = out.head(MAX_ROWS) if ascending else out.tail(MAX_ROWS)
        elif g in d.columns:
            res = d.groupby(g)[col].agg(agg_eff).sort_values(ascending=bool(ascending))
            out = res.head(max(1, min(int(top_n), MAX_ROWS))).reset_index()
            out.columns = [g, f"{agg_eff}_{col}"]
        else:
            return f"Cannot group by '{group_by}'. Use a column ({list(d.columns)}) or one of {list(TIME_GROUPS)}.", None
    except Exception as e:
        return f"Query failed: {e}", None

    return out.to_string(index=False), out


def make_tool(df, log):
    """Create the callable handed to Gemini. `log` collects what was run."""

    def query_sales(metric: str = "sales", agg: str = "sum", group_by: str = "",
                    region: str = "", category: str = "", start_date: str = "",
                    end_date: str = "", top_n: int = 10, ascending: bool = False) -> str:
        """Aggregate the sales dataset and return the exact numbers.

        Args:
            metric: sales, profit, quantity, orders or customers.
            agg: sum, mean, median, max, min, count or nunique (ignored for orders/customers).
            group_by: a column name (e.g. region, category, product_name, customer_id)
                or a time bucket: day, week, month, quarter, year. Empty for one overall number.
            region: optional exact region filter.
            category: optional exact category filter.
            start_date: optional YYYY-MM-DD lower bound.
            end_date: optional YYYY-MM-DD upper bound.
            top_n: max groups to return (default 10, max 25).
            ascending: true to get the lowest groups first.
        """
        text, table = execute_query(df, metric, agg, group_by, region, category,
                                    start_date, end_date, top_n, ascending)
        log.append({
            "args": dict(metric=metric, agg=agg, group_by=group_by, region=region,
                         category=category, start_date=start_date, end_date=end_date,
                         top_n=top_n, ascending=ascending),
            "table": table, "text": text,
        })
        return text

    return query_sales


SYSTEM_PROMPT = (
    "You are a sales analyst answering questions about ONE dataset. "
    "Always call the query_sales tool to get exact numbers before answering; never guess or "
    "invent figures. You may call it several times (e.g. compare periods). "
    "If the data cannot answer the question, say so. Be concise, lead with the answer, "
    "quote the specific numbers, and end with one concrete recommendation when relevant.\n\n"
    "Dataset:\n{schema}"
)