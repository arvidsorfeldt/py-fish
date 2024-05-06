import numpy as np
from py_fish.data import load_one_day
from scipy import integrate
import polars as pl


def total_consumption_from_profile(consumption_profile: np.ndarray) -> float:
    return integrate.trapezoid(consumption_profile[:, 1], consumption_profile[:, 0])


def distance_from_profile(speed_profile: np.ndarray) -> float:
    return integrate.trapezoid(speed_profile[:, 1], speed_profile[:, 0])


def custom_speed_profile(
    distance_out: float,
    speed_out: float,
    distance_fishing: float,
    speed_fishing: float,
    distance_in: float,
    speed_in: float,
    time_per_pot: float = 0.4,
    number_of_pots: float = 12.0,
    speed_during_pot: float = 0.7,
) -> np.ndarray:
    time_out = distance_out / speed_out
    time_in = distance_in / speed_in
    profile = np.array([[0, speed_out], [time_out, speed_out]])
    some_time = (
        distance_fishing - speed_during_pot * time_per_pot * number_of_pots
    ) / (speed_fishing * (number_of_pots - 1))
    for _ in range(0, int(number_of_pots) - 1):
        profile = np.vstack((profile, [profile[-1, 0], speed_during_pot]))
        profile = np.vstack(
            (profile, [profile[-1, 0] + time_per_pot, speed_during_pot])
        )
        profile = np.vstack((profile, [profile[-1, 0], speed_fishing]))
        profile = np.vstack((profile, [profile[-1, 0] + some_time, speed_fishing]))
    profile = np.vstack((profile, [profile[-1, 0], speed_during_pot]))
    profile = np.vstack((profile, [profile[-1, 0] + time_per_pot, speed_during_pot]))
    profile = np.vstack((profile, [profile[-1, 0], speed_in]))
    profile = np.vstack((profile, [profile[-1, 0] + time_in, speed_in]))
    return profile


def trim_profile(df: pl.DataFrame) -> pl.DataFrame:
    local_df = df.with_row_index("index")
    first_index = local_df.filter(pl.col("consumption") > 0.0).head(1).select("index")
    last_index = local_df.filter(pl.col("consumption") > 0.0).tail(1).select("index")
    return local_df.filter(pl.col("index").is_between(first_index, last_index)).select(
        ["time", "speed", "consumption"]
    )


def speed_profile_from_data(vessel: str, date: str) -> np.ndarray:
    df = load_one_day(vessel=vessel, date=date)
    if vessel == "fredrika":
        df = trim_profile(df)
    df = df.select(["time", "speed"])
    speed_profile = df.to_numpy()
    speed_profile[:, 0] = (speed_profile[:, 0] - speed_profile[0, 0]) / (3600 * 1e6)
    return speed_profile


def consumption_profile_from_data(vessel: str, date: str) -> np.ndarray:
    df = load_one_day(vessel=vessel, date=date)
    df = trim_profile(df)
    df = df.select(["time", "consumption"])
    consumption_profile = df.to_numpy()
    consumption_profile[:, 0] = (
        consumption_profile[:, 0] - consumption_profile[0, 0]
    ) / (3600 * 1e6)
    return consumption_profile


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
    down_threshold: float = 3.0,
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
