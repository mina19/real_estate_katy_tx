import glob

import pandas as pd


def raw_filenames(rel_dir: str = "../data/raw/*") -> list:
    """Returns the raw data filenames in a list"""
    raw_data_filenames = glob.glob(rel_dir)
    raw_data_filenames = [file for file in raw_data_filenames if file.endswith(".csv")]
    return raw_data_filenames


def raw_data(raw_data_filenames: list) -> pd.DataFrame:
    """Returns the raw data in a dataframe"""
    raw_df = pd.DataFrame()
    for file in raw_data_filenames:
        df = pd.read_csv(file)
        mask = df["SALE TYPE"] == "PAST SALE"
        raw_df = pd.concat([raw_df, df[mask]])

    return raw_df
