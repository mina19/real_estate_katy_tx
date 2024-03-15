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
        raw_df = pd.concat([raw_df, df[mask]], ignore_index=True)

    return raw_df


def prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    col_names = [column.lower().replace(" ", "_") for column in df.columns]
    df = df.rename(columns=dict(zip(df.columns, col_names)))
    df = df.drop(col_names[-10:], axis=1)
    df = df.rename(
        columns={
            "zip_or_postal_code": "zip_code",
            "$/square_feet": "price_per_square_feet",
            "hoa/month": "hoa_per_month",
        }
    )
    mask = df["property_type"] == "Single Family Residential"
    df = df[mask]

    mask = df["city"] == "Katy"
    df = df[mask]

    df = df.drop(
        [
            "property_type",
            "city",
            "sale_type",
            "days_on_market",
            "state_or_province",
            "sold_date",
        ],
        axis=1,
    )
    return df.reset_index(drop=True)
