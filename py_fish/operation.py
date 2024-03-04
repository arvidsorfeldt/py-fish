import numpy as np
import matplotlib.pyplot as plt
import datetime
from py_fish.data import load_one_day


def speed_profile_from_data(date: str) -> np.ndarray:
    df = load_one_day(date=date)
    df = df.select(["time", "speed"])
    speed_profile = df.to_numpy()
    return speed_profile


def plot_speed_profile(speed_profile: np.ndarray) -> None:
    fig, ax = plt.subplots()
    ax.plot(
        speed_profile[:, 0],
        speed_profile[:, 1],
    )
