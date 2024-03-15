import pandas as pd
import numpy as np
import glob

def raw_filenames(rel_dir: str="../data/raw/*") -> list:
    """Returns the raw data filenames in a list"""
    raw_data_filenames = glob.glob(rel_dir)
    raw_data_filenames = [file for file in raw_data_filenames if file.endswith('.csv')]
    return raw_data_filenames
