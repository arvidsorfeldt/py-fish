from py_fish.engine import EngineApplication, calculate_consumption
from py_fish.data import plot_power, load_one_day, load_all_days
from py_fish.operation import speed_profile_from_data, plot_speed_profile
import numpy as np
import matplotlib.pyplot as plt


print(
    calculate_consumption(
        engine_application=EngineApplication.DEFAULT,
        engine_rating=60,
        powers=np.array([120, 130, 140]),
    )
)
print(
    calculate_consumption(
        engine_application=EngineApplication.CUSTOM,
        engine_rating=60,
        powers=np.array([120, 130, 140]),
        idle_fuel_consumption=0.3,
        bsfc=0.070,
    )
)

load_one_day("2023-10-23")
load_all_days()
plot_power()
plot_speed_profile(speed_profile_from_data("2023-10-23"))

plt.show()
