from enum import Enum, auto
import numpy as np
from py_fish.utils import LITER_PER_GALLON, HP_PER_KW


class EngineApplication(Enum):
    DEFAULT = auto()
    PROPULSION = auto()
    PROPULSION_ZERO_IDLE = auto()
    GENSET = auto()
    CUSTOM = auto()
    IDLE_ONLY = auto()


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
            idle_fuel_consumption = c0 + c1 * engine_rating * HP_PER_KW
            bsfc = c2 + c3 * engine_rating * HP_PER_KW
        case EngineApplication.GENSET:
            c0, c1, c2, c3 = 0.45, 0.0, 0.061, 0
            idle_fuel_consumption = c0 + c1 * engine_rating * HP_PER_KW
            bsfc = c2 + c3 * engine_rating * HP_PER_KW
        case EngineApplication.CUSTOM:
            idle_fuel_consumption = kwargs["idle_fuel_consumption"]
            bsfc = kwargs["bsfc"]
        case EngineApplication.PROPULSION_ZERO_IDLE:
            c0, c1, c2, c3 = 0.26, 8.1e-4, 0.080, -2.1e-5
            idle_fuel_consumption = 0.0
            bsfc = c2 + c3 * engine_rating * HP_PER_KW
        case EngineApplication.IDLE_ONLY:
            c0, c1, c2, c3 = 0.26, 8.1e-4, 0.080, -2.1e-5
            idle_fuel_consumption = c0 + c1 * engine_rating * HP_PER_KW
            bsfc = 0.0
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
            idle_fuel_consumption = c0 + c1 * engine_rating * HP_PER_KW
            bsfc = c2 + c3 * engine_rating * HP_PER_KW
        case EngineApplication.GENSET:
            c0, c1, c2, c3 = 0.45, 0.0, 0.061, 0
            idle_fuel_consumption = c0 + c1 * engine_rating * HP_PER_KW
            bsfc = c2 + c3 * engine_rating * HP_PER_KW
        case EngineApplication.CUSTOM:
            idle_fuel_consumption = kwargs["idle_fuel_consumption"]
            bsfc = kwargs["bsfc"]
        case EngineApplication.PROPULSION_ZERO_IDLE:
            c0, c1, c2, c3 = 0.26, 8.1e-4, 0.080, -2.1e-5
            idle_fuel_consumption = 0.0
            bsfc = c2 + c3 * engine_rating * HP_PER_KW
    return np.maximum(
        (consumptions / LITER_PER_GALLON - idle_fuel_consumption) / bsfc,
        [0] * len(consumptions),
    )


def idle_port_consumption_mira(engine_rating: float, profile: np.ndarray) -> float:
    c0, c1, c2, c3 = 0.26, 8.1e-4, 0.080, -2.1e-5
    idle_fuel_consumption = c0 + c1 * engine_rating * HP_PER_KW
    consumption = 0
    (rows, _) = np.shape(profile)
    for i in range(1, rows):
        (speed, longitude, latitude) = profile[i, [1, 2, 3]]
        if (
            longitude > 11.213
            and longitude < 11.287
            and latitude > 58.580
            and latitude < 58.611
            and speed < 0.1
        ):
            consumption = consumption + idle_fuel_consumption * LITER_PER_GALLON * (
                profile[i, 0] - profile[i - 1, 0]
            )
    return consumption
