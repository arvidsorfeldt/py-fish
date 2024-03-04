from enum import Enum, auto
import numpy as np


class EngineApplication(Enum):
    DEFAULT = auto()
    PROPULSION = auto()
    GENSET = auto()


def calculate_consumption(
    engine_application: EngineApplication, engine_rating: float, powers: np.ndarray
) -> np.ndarray:
    idle_fuel_consumption: float = None
    bsfc: float = None
    match engine_application:
        case EngineApplication.DEFAULT:
            idle_fuel_consumption = 0.49
            bsfc = 0.070
        case EngineApplication.PROPULSION:
            c0, c1, c2, c3 = 0.26, 8.1e-4, 0.080, -2.1e-5
            idle_fuel_consumption = c0 + c1 * engine_rating
            bsfc = c2 + c3 * engine_rating
        case EngineApplication.GENSET:
            c0, c1, c2, c3 = 0.45, 0.0, 0.061, 0
            idle_fuel_consumption = c0 + c1 * engine_rating
            bsfc = c2 + c3 * engine_rating
    return idle_fuel_consumption + bsfc * powers
