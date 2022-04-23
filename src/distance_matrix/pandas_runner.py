import pandas as pd


def run(path: str) -> None:
    df = pd.read_csv(path)
    print(df)
