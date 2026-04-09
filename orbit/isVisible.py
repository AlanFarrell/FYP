from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef
from orbit.HelperFucntions.LineOfSight import ecef_los_to_levation
from orbit.HelperFucntions.LineOfSight import MASK_ANGLE_DEG

def visibility_check(r_teme, jd, fr, lat, lon, alt_m = 0.0):

    #converting satellite TEME to ECEF
    sx, sy, sz = teme_to_ecef(r_teme, jd, fr)

    #putting ground location into EFEC
    gx, gy, gz = LatLonToECEF(lat, lon, alt_m)

    #LOS in ecef
    dx = sx - gx
    dy = sy - gy
    dz = sz - gz

    elev = ecef_los_to_levation(dx, dy, dz, lat, lon)

    return elev >= MASK_ANGLE_DEG, elev






