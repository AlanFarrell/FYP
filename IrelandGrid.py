from math import sin, cos, sqrt, atan2, radians, degrees, fmod, pi

def latlonToCartesian(lat_deg, lon_deg, alt_m = 0.0):
    a = 6378137.0  # WGS84 equatorial radius
    f = 1/298.257223563
    e2 = f*(2-f)

    lat = radians(lat_deg)
    lon = radians(lon_deg)

    sinlat = sin(lat)
    coslat = cos(lat)
    sinlon = sin(lon)
    coslon = cos(lon)

    N = a / sqrt(1 - e2 * sinlat * sinlat)

    x = (N +alt_m) * coslat * coslon
    y = (N +alt_m) * coslat * sinlon
    z = (N *(1-e2) + alt_m) * sinlat

    return x/1000, y/1000, z/1000
