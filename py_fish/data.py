import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from py_fish.loads import calculate_propulsion_power
from pathlib import Path


def load_one_day(vessel: str, date: str) -> pl.DataFrame:
    data_dir = Path(__file__).resolve().parent / vessel
    file_name = "all" + date + ".csv"
    file_path = data_dir / file_name
    df = pl.read_csv(
        file_path, dtypes=[pl.Datetime, pl.Float64, pl.Float64, pl.Float64, pl.Float64]
    )
    df = df.fill_nan(0)
    return df


def load_all_days(vessel: str) -> pl.DataFrame:
    data_dir = Path(__file__).resolve().parent / vessel
    files = [f for f in data_dir.iterdir() if f.is_file()]
    df = pl.concat(
        [
            pl.read_csv(
                f, dtypes=[pl.Datetime, pl.Float64, pl.Float64, pl.Float64, pl.Float64]
            )
            for f in files
        ]
    )
    df = df.fill_nan(0)
    return df


def extract_low_acceleration(speed_and_consumption: np.ndarray) -> np.ndarray:
    acceleration = np.append(np.diff(speed_and_consumption[:, 0]), 0)
    threshold = 0.001
    return speed_and_consumption[np.abs(acceleration) < threshold, :]
