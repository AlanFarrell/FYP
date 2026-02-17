from orbit.gstime_vallado import gstime_vallado
from math import cos, sin
from sgp4.functions import jday


def teme_to_ecef(r_teme, jd, fr):
    """TEME -> ECEF using GMST rotation about earths z axis"""

    theta = gstime_vallado(jd + fr)  # radians
    ct, st = cos(theta), sin(theta)
    x, y, z = r_teme


    # ECEF = Rz(+theta) * TEME
    x_ecef =  ct * x + st * y
    y_ecef = -st * x + ct * y
    z_ecef =  z
    return (x_ecef, y_ecef, z_ecef)
