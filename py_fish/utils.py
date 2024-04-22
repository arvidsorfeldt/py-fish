import numpy as np

FEET_PER_METRE = 3.2808399
LITER_PER_GALLON = 3.78541178
HP_PER_KW = 1.34102209


def components_to_profile(
    first_column: np.ndarray, second_column: np.ndarray
) -> np.ndarray:
    return np.column_stack((first_column, second_column))
