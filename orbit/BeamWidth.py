import numpy as np
from math import degrees, acos
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from orbit.HelperFucntions.gstime_vallado import gstime_vallado

def BeamFilter(sats, jd, fr, obs_lat, obs_lon, obs_alt, beamwidth_deg):
    half_angle = beamwidth_deg/2
    kept = []

    #convert observer LatLon to ECEF then TEME
    observer_ecef = np.array(LatLonToECEF(obs_lat, obs_lon, obs_alt))
    gmst = gstime_vallado(jd + fr)

    ct, st = np.cos(gmst), np.sin(gmst)

    rotation_matrix = np.array([
        [ct, -st, 0.0],
        [st, ct, 0.0],
        [0.0, 0.0, 1.0]
    ])

    observer_teme = rotation_matrix @ observer_ecef

    for sat in sats:
        sat_eci = np.array(sat["position_km"], dtype=float)

        #unit verctor pointing from satellite to earths center
        u_beam = -sat_eci/np.linalg.norm(sat_eci)
        #Line of sight vector
        v_los = observer_teme - sat_eci
        #unit LOS
        u_los = v_los / np.linalg.norm(v_los)
        cosang = np.dot(u_beam, u_los)
        cosang = np.clip(cosang, -1.0, 1.0)
        theta = degrees(acos(cosang))

        if theta <= half_angle:
            kept.append((theta, sat))

    if not kept:
        return [], None

    kept.sort()
    best = kept[0][1]
    filtered = [sat for _, sat in kept]

    return filtered, best


