"""Regenerates the README 'Key findings' charts from data/Sample - Superstore.csv.

Run from the repo root:  python Scripts/make_findings_charts.py
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = "data/Sample - Superstore.csv"
OUT = "images/findings"
BLUE, RED, GREY = "#2563eb", "#dc2626", "#94a3b8"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left"})

df = pd.read_csv(SRC, encoding="latin-1")
df["d"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png", dpi=150)
    plt.close(fig)


# 1. Profit margin by discount band
df["band"] = pd.cut(df["Discount"], [-0.01, 0, 0.2, 0.4, 1], labels=["No discount", "1-20%", "21-40%", ">40%"])
g = df.groupby("band", observed=True)[["Profit", "Sales"]].sum()
margin = g.Profit / g.Sales * 100
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(margin.index.astype(str), margin.values, color=[BLUE if v >= 0 else RED for v in margin])
ax.axhline(0, color="black", lw=0.8)
ax.bar_label(bars, fmt="%.1f%%", padding=3)
ax.set_ylim(min(margin) - 15, max(margin) + 10)
ax.set_ylabel("Profit margin (%)")
ax.set_title("Deep discounts turn profit into loss")
save(fig, "1_discount_margin")

# 2. Profit by sub-category
s = df.groupby("Sub-Category").Profit.sum().sort_values()
fig, ax = plt.subplots(figsize=(7, 5.5))
ax.barh(s.index, s.values / 1000, color=[RED if v < 0 else BLUE for v in s])
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Total profit ($K)")
ax.set_title("Three sub-categories lose money")
save(fig, "2_subcategory_profit")

# 3. Share of sales vs share of profit by category
c = df.groupby("Category")[["Sales", "Profit"]].sum()
c = c / c.sum() * 100
fig, ax = plt.subplots(figsize=(7, 4))
x = range(len(c))
w = 0.38
b1 = ax.bar([i - w / 2 for i in x], c.Sales, w, label="Share of sales", color=GREY)
b2 = ax.bar([i + w / 2 for i in x], c.Profit, w, label="Share of profit", color=BLUE)
ax.bar_label(b1, fmt="%.0f%%", padding=2)
ax.bar_label(b2, fmt="%.0f%%", padding=2)
ax.set_xticks(list(x), c.index)
ax.set_ylabel("% of total")
ax.legend(frameon=False)
ax.set_title("Furniture: a third of sales, 6% of profit")
save(fig, "3_category_share")

# 4. Margin by region: all orders vs orders with discount of 20% or less
def margin_by_region(frame):
    t = frame.groupby("Region")[["Profit", "Sales"]].sum()
    return t.Profit / t.Sales * 100

all_m = margin_by_region(df)
low_m = margin_by_region(df[df["Discount"] <= 0.2])
order = all_m.sort_values().index
fig, ax = plt.subplots(figsize=(7.5, 4))
x = range(len(order))
w = 0.38
b1 = ax.bar([i - w / 2 for i in x], all_m[order], w, label="All orders", color=GREY)
b2 = ax.bar([i + w / 2 for i in x], low_m[order], w, label="Discount of 20% or less", color=BLUE)
ax.bar_label(b1, fmt="%.1f%%", padding=2)
ax.bar_label(b2, fmt="%.1f%%", padding=2)
ax.set_xticks(list(x), order)
ax.set_ylabel("Profit margin (%)")
ax.set_ylim(0, 32)
ax.legend(frameon=False, loc="upper left", ncol=2)
ax.set_title("Central's low margin is a discounting problem")
save(fig, "4_region_margin")

# 5. Seasonality
mo = df.groupby(df.d.dt.month).Sales.sum()
mo = mo / mo.sum() * 100
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.bar(labels, mo.values, color=[BLUE if i in (9, 11, 12) else GREY for i in mo.index])
ax.set_ylabel("% of total sales")
ax.set_title("Sep, Nov and Dec drive 43% of sales")
save(fig, "5_seasonality")
print("done")
