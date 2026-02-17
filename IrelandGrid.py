from math import sin, cos, sqrt, atan2, radians, degrees, fmod, pi

def latlonToCartesian(lat : float, lon : float):
    #Function which takes lat and lon co-ords and converts first into radians
    #then converts the radians co-ord into x, y ,z values - with center of earth being the origin
    R = 6371

    lat_r = radians(lat)
    lon_r = radians(lon)

    x = R*cos(lat_r)*cos(lon_r)
    y = R*cos(lat_r)*sin(lon_r)
    z = R*sin(lat_r)
    return x,y,z
