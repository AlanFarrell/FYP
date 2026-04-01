def is_DTC(norad_id):
    """
    Returns True if this NORAD ID belongs to a Direct-To-Cell Starlink satellite.
    """
    DTC_ranges = [
        range(59000, 59200),
        range(59500, 59600),
    ]

    return any(norad_id in r for r in DTC_ranges)