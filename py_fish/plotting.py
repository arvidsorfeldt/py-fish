import numpy as np


def plot_speed_profile(speed_profile: np.ndarray, ax) -> None:
    ax.plot(
        speed_profile[:, 0],
        speed_profile[:, 1],
    )
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Speed [kn]")


def plot_profiles(ax, *args) -> None:
    for arg in args:
        ax.plot(arg[:, 0], arg[:, 1])


def plot_consumption_data(speed_and_consumption: np.ndarray, ax, label: str) -> None:
    ax.scatter(
        speed_and_consumption[:, 0], speed_and_consumption[:, 1], s=2, label=label
    )
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 50])
    ax.set_xlabel("Speed [kn]")
    ax.set_ylabel("Consumption [l/h]")
