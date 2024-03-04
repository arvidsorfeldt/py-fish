from py_fish.engine import EngineApplication, calculate_consumption
from py_fish.data import plot_power, load_one_day


print(calculate_consumption(EngineApplication.DEFAULT, 60, 120))
load_one_day("2023-10-23")
plot_power()
