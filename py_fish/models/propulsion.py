from math import sqrt, exp, pow
from py_fish.utils import FEET_PER_METRE


def caclulate_power(length: float, beam: float, speed: float) -> float:
    c4, c14 = 3.6e-3, 0.57
    return (
        pow((min(speed, 3) / 3), 3)
        * length
        * FEET_PER_METRE
        * sqrt(beam * FEET_PER_METRE)
        * c4
        * exp(speed * c14)
    )
