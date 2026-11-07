import io

import pandas as pd


def load_sales(csv_text):
    df = pd.read_csv(io.StringIO(csv_text))
    df = df.dropna(subset=["units"])
    df = df.assign(date=pd.to_datetime(df["date"]))
    df = df.assign(revenue=df["units"] * df["price"])
    return df.reset_index(drop=True)


def revenue_by_month(df):
    months = df["date"].dt.strftime("%Y-%m")
    totals = df.groupby(months)["revenue"].sum().round(2)
    return {month: float(total) for month, total in totals.items()}


def best_products(df, n):
    totals = df.groupby("product")["revenue"].sum().nlargest(n)
    return [(product, round(float(total), 2)) for product, total in totals.items()]


def report(df):
    total = df["revenue"].sum()
    best = best_products(df, 1)[0][0]
    months = revenue_by_month(df)
    busiest = max(months, key=months.get)
    return f"Total revenue: ${total:.2f}\nBest product: {best}\nBusiest month: {busiest}"
