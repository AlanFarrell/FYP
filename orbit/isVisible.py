from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef
from orbit.HelperFucntions.LineOfSight import ecef_los_to_levation
from orbit.HelperFucntions.LineOfSight import MASK_ANGLE_DEG

def visibility_check(r_ecef, g_ecef, lat, lon):


    sx, sy, sz = r_ecef
    gx, gy, gz = g_ecef

    #LOS in ecef
    dx = sx - gx
    dy = sy - gy
    dz = sz - gz

    elev = ecef_los_to_levation(dx, dy, dz, lat, lon)

    return elev >= MASK_ANGLE_DEG, elev