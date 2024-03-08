from enum import Enum, auto
import numpy as np
from py_fish.utils import LITER_PER_GALLON


class EngineApplication(Enum):
    DEFAULT = auto()
    PROPULSION = auto()
    GENSET = auto()
    CUSTOM = auto()


def calculate_consumption(
    engine_application: EngineApplication,
    engine_rating: float,
    powers: np.ndarray,
    **kwargs,
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
        case EngineApplication.CUSTOM:
            idle_fuel_consumption = kwargs["idle_fuel_consumption"]
            bsfc = kwargs["bsfc"]
    return (idle_fuel_consumption + bsfc * powers) * LITER_PER_GALLON


def calculate_power_from_consumption(
    engine_application: EngineApplication,
    engine_rating: float,
    consumptions: np.ndarray,
    **kwargs,
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
        case EngineApplication.CUSTOM:
            idle_fuel_consumption = kwargs["idle_fuel_consumption"]
            bsfc = kwargs["bsfc"]
    return np.max((consumptions / LITER_PER_GALLON - idle_fuel_consumption) / bsfc, 0)
