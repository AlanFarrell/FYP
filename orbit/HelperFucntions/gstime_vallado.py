import math

def gstime_vallado(jdut1: float) -> float:
    T = (jdut1 - 2451545.0) / 36525.0
    gmst_sec = (
        67310.54841
        + (876600.0 * 3600 + 8640184.812866) * T
        + 0.093104 * (T**2)
        - 6.2e-6 * (T**3)
    )
    gmst_sec %= 86400.0
    if gmst_sec < 0:
        gmst_sec += 86400.0
    return (gmst_sec / 86400.0) * 2.0 * math.pi