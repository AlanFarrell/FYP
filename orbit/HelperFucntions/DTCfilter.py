def is_DTC(tle_line2):


    """
    Returns True if this TLE belongs to a Direct-To-Cell Starlink satellite.
    Identifies DTC satellites by inclination (53° and 43° shells).
    """

    fields = tle_line2.split()
    inc = float(fields[2])
    ecc = float("0." + fields[4].lstrip("0"))

    if ecc > 0.00030:
        return False

    if 52.8 <= inc <= 53.4:
        return True
    if 42.8 <= inc <= 43.4:
        return True

    return False

