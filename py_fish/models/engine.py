from enum import Enum, auto


class EngineApplication(Enum):
    DEFAULT = auto()
    PROPULSION = auto()
    GENSET = auto()


class Engine:
    def __init__(
        self, engine_application: EngineApplication, engine_rating: float
    ) -> None:
        """
        Engine
        ------

        Args:
            engine_application (EngineApplication): The engine application
            engine_rating (float): The engine power rating in kW
        """
        match engine_application:
            case EngineApplication.DEFAULT:
                self.idle_fuel_consumption = 0.49
                self.bsfc = 0.070
                self.engine_rating = engine_rating
            case EngineApplication.PROPULSION:
                c0, c1, c2, c3 = 0.26, 8.1e-4, 0.080, -2.1e-5
                self.idle_fuel_consumption = c0 + c1 * engine_rating
                self.bsfc = c2 + c3 * engine_rating
                self.engine_rating = engine_rating
            case EngineApplication.GENSET:
                c0, c1, c2, c3 = 0.45, 0.0, 0.061, 0
                self.idle_fuel_consumption = c0 + c1 * engine_rating
                self.bsfc = c2 + c3 * engine_rating
                self.engine_rating = engine_rating

    def calculate_consumption(self, power: float) -> float:
        return self.idle_fuel_consumption + self.bsfc * power

    def __str__(self) -> str:
        return (
            "Engine with\n  alpha = "
            + str(self.idle_fuel_consumption)
            + "\n  beta = "
            + str(self.bsfc)
        )
