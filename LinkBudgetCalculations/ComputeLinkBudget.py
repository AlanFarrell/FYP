import numpy as np
from numpy import ndarray


from config import LinkBudgetConfig, ContentionConfig
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from LinkBudgetCalculations.linkbudget import LinkBudgetCalculations
from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef


def compute_slant_range(satellite_ecef, observer_ecef):
    return np.linalg.norm(satellite_ecef - observer_ecef)

def contention_model(capacity_mbps):
        return capacity_mbps / ContentionConfig.NUM_USERS


def compute_link_budget(optimal_satellite, interferers, jd, fr, lat, lon, other_losses_db: float = 0.0):
    transmit_power_db = LinkBudgetConfig.TRANSMIT_POWER_DB
    receiver_gain_dbi = LinkBudgetConfig.RECEIVER_GAIN_DBI
    frequency_hz = LinkBudgetConfig.FREQUENCY_HZ
    interference_watts = LinkBudgetConfig.OTHER_LOSSES_DB

    if optimal_satellite is None:
        return {"capacity_mbps": 0.0}

    link_budget = LinkBudgetCalculations()
    observer_ecef_m = np.array(LatLonToECEF(lat, lon, 0.0))

    satellite_position_km = optimal_satellite["position_km"]
    satellite_ecef_m = np.array(teme_to_ecef(satellite_position_km, jd, fr)) * 1000.0
    slant_range = compute_slant_range(satellite_ecef_m, observer_ecef_m)

    received_signal_watts, path_loss_db = link_budget.received_power_watts(transmit_power_db, receiver_gain_dbi, slant_range, frequency_hz, other_losses_db)
    interference_watts = Compute_interfereance(interferers, jd, fr,
                                               observer_ecef_m,link_budget, frequency_hz, other_losses_db,
                                               transmit_power_db, receiver_gain_dbi, interference_watts)

    link_budget.signal_power_watts = received_signal_watts
    link_budget.interference_power_watts = interference_watts

    results = link_budget.compute()
    raw_capacity = results.capacity_mbps

    if ContentionConfig.USE_CONTENTION:
        adjusted_capacity = contention_model(raw_capacity)
    else:
        adjusted_capacity = raw_capacity


    return {"capacity_mbps": adjusted_capacity}


def Compute_interfereance(interferers, jd, fr, observer_ecef_m:ndarray, link_budget:LinkBudgetCalculations,
                          frequency_hz: float, other_losses_db: float, transmit_power_db: float,
                           receiver_gain_dbi: float, interference_watts: float) -> float:
    for i in interferers:
        position_km = i["position_km"]
        position_ecef_m = np.array(teme_to_ecef(position_km, jd, fr)) * 1000.0
        distance2_m = compute_slant_range(position_ecef_m, observer_ecef_m)
        power_watts, _ = link_budget.received_power_watts(transmit_power_db, receiver_gain_dbi, distance2_m,
                                                          frequency_hz, other_losses_db)
        interference_watts += power_watts * 0.001
    return interference_watts