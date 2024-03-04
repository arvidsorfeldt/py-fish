import numpy as np
import matplotlib.pyplot as plt
import datetime
from py_fish.data import load_one_day


def speed_profile_from_data(date: str) -> np.ndarray:
    df = load_one_day(date=date)
    df = df.select(["time", "speed"])
    speed_profile = df.to_numpy()
    speed_profile[:, 0] = (speed_profile[:, 0] - speed_profile[0, 0]) / (3600 * 1e6)
    return speed_profile


def extract_transit(
    speed_profile: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    passed_7_up = False
    num = len(speed_profile[:, 1])
    first_index = None
    last_index = None

    for i in range(0, num):
        if not passed_7_up and speed_profile[i, 1] > 7:
            passed_7_up = True
        elif passed_7_up and speed_profile[i, 1] < 5:
            first_index = i
            break
    passed_7_up = False
    for i in range(0, num).__reversed__():
        if not passed_7_up and speed_profile[i, 1] > 7:
            passed_7_up = True
        elif passed_7_up and speed_profile[i, 1] < 5:
            last_index = i
            break
    return (
        speed_profile[0:first_index, :],
        speed_profile[first_index:last_index, :],
        speed_profile[last_index:, :],
    )


def plot_speed_profile(speed_profile: np.ndarray) -> None:
    fig, ax = plt.subplots()
    ax.plot(
        speed_profile[:, 0],
        speed_profile[:, 1],
    )
