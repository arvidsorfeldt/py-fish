from py_fish.engine import EngineApplication, calculate_consumption
from py_fish.data import plot_power


print(calculate_consumption(EngineApplication.DEFAULT, 60, 120))
plot_power()
