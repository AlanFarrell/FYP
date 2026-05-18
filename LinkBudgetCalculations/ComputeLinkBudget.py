import numpy as np
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from LinkBudgetCalculations.linkbudget import LinkBudgetCalculations
from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef


USE_CONTENTION = False
NUM_USERS = 20
CONTENTION_METHOD = "equal"


def slant_range_m(satellite_ecef, observer_ecef):
    return np.linalg.norm(satellite_ecef - observer_ecef)

def contention_model(capacity_mbps, num_users = None, method = "equal", sinr_db = None):
    """
    applys a user contention model
    """

    if num_users is None:
        return capacity_mbps

    if method == "equal":
        return capacity_mbps / num_users

    else:
        raise ValueError("Invalid contention method")


def compute_link_budget(optimal_satellite, interferers, jd, fr, lat, lon, other_losses_db: float = 0.0):
    transmit_power_db = 46
    receiver_gain_dbi = 33
    frequency_hz = 12e9
    interference_watts = 0.0

    if optimal_satellite is None:
        return {
            "capacity_mbps": 0.0,
            "sinr_db": -np.inf,
            "fspl_db": None,
            "distance_m": None
        }

    satellite_position_km = optimal_satellite["position_km"]
    satellite_ecef_m = np.array(teme_to_ecef(satellite_position_km, jd, fr)) * 1000.0
    observer_ecef_m = np.array(LatLonToECEF(lat, lon, 0.0))
    distance_m = slant_range_m(satellite_ecef_m, observer_ecef_m)
    link_budget = LinkBudgetCalculations()
    received_signal_watts, path_loss_db = link_budget.received_power_watts(transmit_power_db, receiver_gain_dbi, distance_m, frequency_hz, other_losses_db)

    for i in interferers:
        position_km = i["position_km"]
        position_ecef_m = np.array(teme_to_ecef(position_km, jd, fr)) * 1000.0
        distance2_m = slant_range_m(position_ecef_m, observer_ecef_m)
        power_watts, _ = link_budget.received_power_watts(transmit_power_db, receiver_gain_dbi, distance2_m, frequency_hz, other_losses_db)
        interference_watts += power_watts * 0.001

    link_budget.signal_power_watts = received_signal_watts
    link_budget.interference_power_watts = interference_watts

    results = link_budget.compute()
    raw_capacity = results.capacity_mbps

    if USE_CONTENTION:
        adjusted_capacity = contention_model(
            raw_capacity,
            num_users=NUM_USERS,
            method=CONTENTION_METHOD,
            sinr_db=results.sinr_db
        )
    else:
        adjusted_capacity = raw_capacity

    return {
        "capacity_mbps": adjusted_capacity,
        "raw_capacity_mbps": raw_capacity,
        "sinr_db": results.sinr_db,
        "fspl_db": path_loss_db,
        "distance_m": distance_m,
    }