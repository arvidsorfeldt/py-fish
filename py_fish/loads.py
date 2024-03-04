from math import sqrt, exp, pow
from py_fish.utils import FEET_PER_METRE


def calculate_propulsion_power(length: float, beam: float, speed: float) -> float:
    c4, c14 = 3.6e-3, 0.57
    return (
        pow((min(speed, 3) / 3), 3)
        * length
        * FEET_PER_METRE
        * sqrt(beam * FEET_PER_METRE)
        * c4
        * exp(speed * c14)
    )


def calculate_dc_energy(
    hours_total: float,
    dc_base_load: float = 0.3,
    battery_efficiency: float = 0.8,
    alternator_efficiency: float = 0.6,
):
    return dc_base_load * hours_total / (battery_efficiency * alternator_efficiency)


def calculate_ac_power():
    pass


def calculate_hydraulics_energy(
    hours_fishing: float,
    hydraulic_deck_load_power: float = 4.0,
    duty_cycle: float = 0.48,
    pump_efficiency: float = 0.96,
):
    return duty_cycle * hydraulic_deck_load_power * hours_fishing / pump_efficiency


def calculate_refrigiration_power(average_refrigiration_power: float = 0.0) -> float:
    return average_refrigiration_power
