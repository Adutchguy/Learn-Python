import pandas as pd


def clean_names(df):
    return df.assign(name=df["name"].str.strip().str.title())


def parse_prices(df):
    return df.assign(price=df["price"].str.replace("[$,]", "", regex=True).astype(float))


def fill_missing_scores(df):
    return df.assign(score=df["score"].fillna(df["score"].mean()))


def unique_people(df):
    return df.drop_duplicates(subset=["name"]).reset_index(drop=True)
