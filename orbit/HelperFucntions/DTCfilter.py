def is_likely_dtc(norad_id: int, inclination_deg: float) -> bool:

    """
    Starlink Gen2/V2-Mini launches presumed DTC-capable.

    This is an approximation for coverage simulation, not a definitive classification.
    """

    DTC_NORAD_RANGES = (
        range(59000, 59200),  # Early Gen2 / v2‑Mini launches (2023–early 2024)
        range(59500, 59600),  # Subsequent Gen2 batches
    )

    in_known_batch = any(norad_id in r for r in DTC_NORAD_RANGES)
    gen2_like_orbit = 40 <= inclination_deg <= 55

    return in_known_batch and gen2_like_orbit
