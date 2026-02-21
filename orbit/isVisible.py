from IrelandGrid import latlonToCartesian
from orbit.TEMEtoECEF import teme_to_ecef
from orbit.LineOfSight import ecef_los_to_levation
from orbit.LineOfSight import MASK_ANGLE_DEG

def is_visible(r_teme, jd, fr, lat, lon, alt_m = 0.0):

    #converting satellite TEME to ECEF
    sx, sy, sz = teme_to_ecef(r_teme, jd, fr)

    #putting ground location into EFEC
    gx, gy, gz = latlonToCartesian(lat, lon, alt_m)

    #LOS in ecef
    dx = sx - gx
    dy = sy - gy
    dz = sz - gz

    elev = ecef_los_to_levation(dx, dy, dz, lat, lon)

    return elev >= MASK_ANGLE_DEG, elev






