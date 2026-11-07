import pandas as pd


def total_by_category(df):
    return {key: float(total) for key, total in df.groupby("category")["amount"].sum().items()}


def average_by(df, key, value):
    return {name: float(mean) for name, mean in df.groupby(key)[value].mean().round(2).items()}


def busiest_category(df):
    return df["category"].value_counts().idxmax()


def summary_table(df):
    table = df.groupby("category").agg(count=("amount", "count"), mean=("amount", "mean")).reset_index()
    table["mean"] = table["mean"].round(2)
    return table
