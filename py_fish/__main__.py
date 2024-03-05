from py_fish.engine import EngineApplication, calculate_consumption
from py_fish.data import plot_power, load_one_day, load_all_days
from py_fish.operation import (
    speed_profile_from_data,
    plot_speed_profile,
    general_speed_profile,
    plot_profiles,
    extract_transit_speed,
    consumption_profile_form_data,
    total_consumption_from_profile,
)
import numpy as np
import matplotlib.pyplot as plt

print(total_consumption_from_profile(consumption_profile_form_data("2023-10-23")))
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
plot_speed_profile(
    general_speed_profile(
        transit_speed=8, transit_time=1, fishing_speed=2, fishing_time=6
    )
)

(transit_out, fishing, transit_in) = extract_transit_speed(
    speed_profile_from_data("2023-10-23")
)
plot_profiles(transit_out, fishing, transit_in)

(transit_out, fishing, transit_in) = extract_transit_speed(
    general_speed_profile(
        transit_speed=8, transit_time=1, fishing_speed=2, fishing_time=6
    )
)
plot_profiles(transit_out, fishing, transit_in)

plt.show()
