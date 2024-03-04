import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from py_fish.loads import calculate_propulsion_power
from pathlib import Path


def load_one_day(date: str) -> pl.DataFrame:
    data_dir = Path(__file__).resolve().parent / "data"
    file_name = "all" + date + ".csv"
    file_path = str(data_dir / file_name)
    df = pl.read_csv(
        file_path, dtypes=[pl.Datetime, pl.Float64, pl.Float64, pl.Float64, pl.Float64]
    )
    return df


def plot_power():
    speeds = np.linspace(0, 10)
    power_lambda = lambda speed: calculate_propulsion_power(
        length=12, beam=4, speed=speed
    )
    power_vec = np.vectorize(power_lambda)
    fig, ax = plt.subplots()
    ax.plot(speeds, power_vec(speeds))
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 160])
    ax.set_xlabel("Speed [kn]")
    ax.set_ylabel("Power [kW]")
    fig.tight_layout()
    plt.show()
