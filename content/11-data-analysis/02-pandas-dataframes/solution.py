import pandas as pd


def build_scores(names, points):
    return pd.DataFrame({"name": names, "points": points})


def top_scorer(df):
    best = df["points"].idxmax()
    return df.loc[best, "name"]


def add_bonus(df, bonus):
    return df.assign(total=df["points"] + bonus)


def describe_points(df):
    points = df["points"]
    return {"mean": float(points.mean()), "max": float(points.max()), "min": float(points.min())}
