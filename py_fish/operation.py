import numpy as np
import matplotlib.pyplot as plt
from py_fish.data import load_one_day
from scipy import integrate


def total_consumption_from_profile(consumption_profile: np.ndarray) -> float:
    return integrate.trapezoid(consumption_profile[:, 1], consumption_profile[:, 0])


def speed_profile_from_data(date: str) -> np.ndarray:
    df = load_one_day(date=date)
    df = df.select(["time", "speed"])
    speed_profile = df.to_numpy()
    speed_profile[:, 0] = (speed_profile[:, 0] - speed_profile[0, 0]) / (3600 * 1e6)
    return speed_profile


def consumption_profile_form_data(date: str) -> np.ndarray:
    df = load_one_day(date=date)
    df = df.select(["time", "consumption"])
    consumption_profile = df.to_numpy()
    consumption_profile[:, 0] = (
        consumption_profile[:, 0] - consumption_profile[0, 0]
    ) / (3600 * 1e6)
    return consumption_profile


def general_speed_profile(
    transit_speed: float, transit_time: float, fishing_speed: float, fishing_time: float
) -> np.ndarray:
    return np.array(
        [
            [0, 0],
            [0, transit_speed],
            [transit_time, transit_speed],
            [transit_time, fishing_speed],
            [transit_time + fishing_time, fishing_speed],
            [transit_time + fishing_time, transit_speed],
            [transit_time + fishing_time + transit_time, transit_speed],
            [transit_time + fishing_time + transit_time, 0],
        ]
    )


def _extract_transit(
    profile: np.ndarray,
    up_threshold: float,
    down_threshold: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    passed_7_up = False
    num = len(profile[:, 1])
    first_index = None
    last_index = None

    for i in range(0, num):
        if not passed_7_up and profile[i, 1] > up_threshold:
            passed_7_up = True
        elif passed_7_up and profile[i, 1] < down_threshold:
            first_index = i
            break
    passed_7_up = False
    for i in range(0, num).__reversed__():
        if not passed_7_up and profile[i, 1] > up_threshold:
            passed_7_up = True
        elif passed_7_up and profile[i, 1] < down_threshold:
            last_index = i
            break
    return (
        profile[0 : first_index + 1, :],
        profile[first_index : last_index + 1, :],
        profile[last_index:, :],
    )


def extract_transit_speed(
    speed_profile: np.ndarray,
    up_threshold: float = 7.0,
    down_threshold: float = 5.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return _extract_transit(
        profile=speed_profile, up_threshold=up_threshold, down_threshold=down_threshold
    )


def extract_transit_consumption(
    consumption_profile: np.ndarray,
    up_threshold: float = 20.0,
    down_threshold: float = 8.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return _extract_transit(
        profile=consumption_profile,
        up_threshold=up_threshold,
        down_threshold=down_threshold,
    )
