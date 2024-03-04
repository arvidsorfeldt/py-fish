from py_fish.operation import extract_transit, speed_profile_from_data
from py_fish.data import load_one_day


def test():
    speed_profile = speed_profile_from_data("2023-10-23")
    (transit_out, fishing, transit_in) = extract_transit(speed_profile)
    assert len(speed_profile) == len(transit_out) + len(fishing) + len(transit_in)
