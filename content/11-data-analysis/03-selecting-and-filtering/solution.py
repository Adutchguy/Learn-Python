import pandas as pd


def adults(df):
    return df[df["age"] >= 18]


def names_in_city(df, city):
    mask = (df["age"] >= 18) & (df["city"] == city)
    return df[mask]["name"].tolist()


def select_columns(df, cols):
    return df[cols]


def in_cities(df, cities):
    return df[df["city"].isin(cities)]


def oldest_first(df):
    return df.sort_values("age", ascending=False).reset_index(drop=True)
