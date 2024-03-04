from py_fish.utils import FEET_PER_METRE
import numpy as np


def calculate_propulsion_power(
    length: float, beam: float, speeds: np.ndarray
) -> np.ndarray:
    c4, c14 = 3.6e-3, 0.57
    return (
        np.power((np.minimum(speeds, [3] * len(speeds)) / 3), 3)
        * length
        * FEET_PER_METRE
        * np.sqrt(beam * FEET_PER_METRE)
        * c4
        * np.exp(speeds * c14)
    )


def calculate_dc_energy(
    hours_total: float,
    dc_base_load: float = 0.3,
    battery_efficiency: float = 0.8,
    alternator_efficiency: float = 0.6,
):
    return dc_base_load * hours_total / (battery_efficiency * alternator_efficiency)


def calculate_ac_energy():
    pass


def calculate_hydraulics_energy(
    hours_fishing: float,
    hydraulic_deck_load_power: float = 4.0,
    duty_cycle: float = 0.48,
    pump_efficiency: float = 0.96,
):
    return duty_cycle * hydraulic_deck_load_power * hours_fishing / pump_efficiency


def calculate_refrigiration_energy(
    hours_total: float,
    average_refrigiration_power: float = 0.0,
    duty_cycle: float = 0.0,
) -> float:
    return duty_cycle * average_refrigiration_power * hours_total
