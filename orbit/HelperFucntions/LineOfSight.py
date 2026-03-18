from math import radians, sin, cos, atan2, degrees, sqrt

MASK_ANGLE_DEG = 10

def ecef_los_to_levation(dx, dy, dz, lat_deg, lon_deg):
    lat = radians(lat_deg)
    lon = radians(lon_deg)
    slat, clat = sin(lat), cos(lat)
    slon, clon = sin(lon), cos(lon)

    e = -slon * dx + clon * dy
    n = -clon*slat * dx - slon*slat * dy + clat * dz
    u=  clon*clat * dx + slon*clat * dy + slat * dz


    horiz = sqrt(e*e + n*n)
    elev_rad = atan2(u, horiz)

    return degrees(elev_rad)

