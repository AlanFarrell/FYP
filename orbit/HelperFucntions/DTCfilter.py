def is_DTC(norad_id):


    """
    Returns True if this TLE belongs to a Direct-To-Cell Starlink satellite.
    """
    def is_DTC(norad_id):
        DTC_batch = [
            range(59000, 59200),
            range(59500, 59600),
        ]

        return any(norad_id in batch for batch in DTC_batch)