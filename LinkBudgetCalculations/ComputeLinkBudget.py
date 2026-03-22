import numpy as np
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from LinkBudgetCalculations.linkbudget import LinkBudgetCalculations
from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef


def slant_range_m(satellite_ecef, observer_ecef):
    return np.linalg.norm(satellite_ecef - observer_ecef)

def compute_link_budget(optimal_satellite, interferers, jd, fr, lat, lon):

    #PLACEHOLDER VALUES -> TO BE CHANGED
    transmit_power_db = 58
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


    received_signal_watts, path_loss_db = link_budget.received_power_watts(transmit_power_db, receiver_gain_dbi, distance_m, frequency_hz)

    for i in interferers:
        position_km = i["position_km"]
        position_ecef_m = np.array(teme_to_ecef(position_km, jd, fr)) * 1000.0

        distance2_m = slant_range_m(position_ecef_m, observer_ecef_m)

        power_watts, _ = link_budget.received_power_watts(transmit_power_db, receiver_gain_dbi, distance2_m, frequency_hz)
        interference_watts += power_watts * 0.001

    link_budget.signal_power_watts = received_signal_watts
    link_budget.interference_power_watts = interference_watts

    results = link_budget.compute()

    return {
        "capacity_mbps": results.capacity_mbps,
        "sinr_db": results.sinr_db,
        "fspl_db": path_loss_db,
        "distance_m": distance_m,
    }
