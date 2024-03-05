from py_fish.operation import extract_transit_speed, speed_profile_from_data


def test():
    speed_profile = speed_profile_from_data("2023-10-23")
    (transit_out, fishing, transit_in) = extract_transit_speed(speed_profile)
    assert len(speed_profile) + 2 == len(transit_out) + len(fishing) + len(transit_in)
