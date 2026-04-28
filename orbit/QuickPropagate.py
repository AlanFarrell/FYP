from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from sgp4.api import Satrec
from datetime import datetime, timedelta, timezone


def quickPropagate(TLEs, duration, step, start_time_utc=None):
    """
    Propagate all satellites from TLEs for a given duration.

    -------
    dict
        {
            "sat_name": [
                {"time": datetime, "r": (x,y,z)},
                ...
            ]
        }
    """

    satellites = [
        (name.strip(), Satrec.twoline2rv(line1.strip(), line2.strip()))
        for name, line1, line2 in TLEs
    ]

    if start_time_utc is None:
        start_time_utc = datetime.now(timezone.utc)
    elif start_time_utc.tzinfo is None:
        raise ValueError("start_time_utc must be timezone-aware (UTC)")

    end_time = start_time_utc + timedelta(hours=duration)
    step_td = timedelta(seconds=step)
    propagated = {name: [] for name, _ in satellites}

    current_time = start_time_utc
    while current_time < end_time:
        jd, fr = GetJulianDate(current_time)

        for name, sat in satellites:
            e, r, v = sat.sgp4(jd, fr)
            if e == 0:
                propagated[name].append({
                    "time": current_time,
                    "r": r,
                })

        current_time += step_td

    return propagated