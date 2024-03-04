import numpy as np
import matplotlib.pyplot as plt
from py_fish.loads import calculate_propulsion_power


def plot_power():
    speeds = np.linspace(0, 10)
    power_lambda = lambda speed: calculate_propulsion_power(
        length=12, beam=4, speed=speed
    )
    power_vec = np.vectorize(power_lambda)
    plt.plot(speeds, power_vec(speeds))
    # fig.tight_layout()
    plt.show()
