from py_fish.models.engine import EngineApplication, calculate_consumption
from py_fish.models.data import plot_power


print(calculate_consumption(EngineApplication.DEFAULT, 60, 120))
plot_power()
