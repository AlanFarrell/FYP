import numpy as np
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from orbit.HelperFucntions.gstime_vallado import gstime_vallado

from config import SimulationConfig

def BeamFilter(propagated_satellites, obs_lat, obs_lon, obs_alt):
    if len(propagated_satellites) == 0:
        return [], None

    half_angle = SimulationConfig.BEAMWIDTH/2

    #convert observer LatLon to ECEF then TEME
    observer_ecef = np.array(LatLonToECEF(obs_lat, obs_lon, obs_alt))

    satellite_positions = np.array([s["position_km"] for s in propagated_satellites])

    #compute beam unit vectors
    satellite_normalised = np.linalg.norm(satellite_positions, axis=1, keepdims=True)
    u_beam = -satellite_positions / satellite_normalised

    #line of sight vectors
    v_los = observer_ecef - satellite_positions
    v_los_normalised = np.linalg.norm(v_los, axis=1, keepdims=True)
    u_los = v_los / v_los_normalised

    #angle between beam and LOS
    cosang = np.sum(u_beam * u_los, axis=1)
    cosang = np.clip(cosang, -1.0, 1.0)

    theta = np.degrees(np.arccos(cosang))
    keep_mask = theta <= half_angle
    satellites_array = np.array(propagated_satellites, dtype=object)

    if not np.any(keep_mask):
        return [], None

    kept_satellites = satellites_array[keep_mask]
    best_sattelite = kept_satellites[np.argmin(theta[keep_mask])]

    return list(kept_satellites), best_sattelite
