import glob

import pandas as pd


def raw_filenames(rel_dir: str = "../data/raw/*") -> list:
    """Returns the raw data filenames in a list"""
    raw_data_filenames = glob.glob(rel_dir)

    # Ignore the README.md file
    raw_data_filenames = [file for file in raw_data_filenames if file.endswith(".csv")]
    return raw_data_filenames


def raw_data(raw_data_filenames: list) -> pd.DataFrame:
    """Returns the raw data in a dataframe"""
    raw_df = pd.DataFrame()
    for file in raw_data_filenames:
        df = pd.read_csv(file)

        # Remove header line that says
        # 'In accordance with local MLS rules, some MLS listings are not included in the download'
        # in the SALE TYPE column
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

    # Remove townhomes from analysis
    mask = df["property_type"] == "Single Family Residential"
    df = df[mask]

    # Only interested in Katy
    mask = df["city"] == "Katy"
    df = df[mask]

    df = df.drop(
        [
            "property_type",  # all the same
            "city",  # all the same
            "sale_type",  # all the same
            "days_on_market",  # unavailable
            "state_or_province",  # all the same
            "sold_date",  # not important (may be cool to see how this is related to interested rates)
        ],
        axis=1,
    )
    return df.reset_index(drop=True)
