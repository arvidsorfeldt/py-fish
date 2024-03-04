import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from py_fish.loads import calculate_propulsion_power
from pathlib import Path


def load_one_day(date: str) -> pl.DataFrame:
    data_dir = Path(__file__).resolve().parent / "data"
    file_name = "all" + date + ".csv"
    file_path = data_dir / file_name
    df = pl.read_csv(
        file_path, dtypes=[pl.Datetime, pl.Float64, pl.Float64, pl.Float64, pl.Float64]
    )
    return df


def load_all_days() -> pl.DataFrame:
    data_dir = Path(__file__).resolve().parent / "data"
    files = [f for f in data_dir.iterdir() if f.is_file()]
    df = pl.concat(
        [
            pl.read_csv(
                f, dtypes=[pl.Datetime, pl.Float64, pl.Float64, pl.Float64, pl.Float64]
            )
            for f in files
        ]
    )
    return df


def plot_power():
    speeds = np.linspace(0, 10)
    power = calculate_propulsion_power(length=12, beam=4, speeds=speeds)

    fig, ax = plt.subplots()
    ax.plot(speeds, power)
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 160])
    ax.set_xlabel("Speed [kn]")
    ax.set_ylabel("Power [kW]")
    fig.tight_layout()

    df = load_all_days()
    fig2, ax2 = plt.subplots()
    ax2.scatter(df.select("speed"), df.select("consumption"))
    ax2.set_xlim([0, 10])
    ax2.set_ylim([0, 50])
    ax2.set_xlabel("Speed [kn]")
    ax2.set_ylabel("Consumption [l/h]")
    fig2.tight_layout()
