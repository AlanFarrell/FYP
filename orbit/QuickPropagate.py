from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from sgp4.api import Satrec
from datetime import datetime, timedelta, timezone
from config import SimulationConfig


def quickPropagate(TLEs):
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

    end_time = SimulationConfig.SIMULATION_START + timedelta(hours=SimulationConfig.SIMULATION_DURATION_HOURS)
    step_td = timedelta(seconds=SimulationConfig.PROPAGATION_TIME_STEP)
    propagated = {name: [] for name, _ in satellites}

    current_time = SimulationConfig.SIMULATION_START
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