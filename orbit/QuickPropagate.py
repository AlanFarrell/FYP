from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from sgp4.api import Satrec
from datetime import datetime, timedelta, timezone


def quickPropagate(TLEs, duration, step):
    """
       Propagate all satellites from TLEs for 24 hours ahead.
       Returns a dictionary:
       {
           "sat_name": [
               {"time": datetime, "r": (x,y,z), "v": (vx,vy,vz)},
               ...
           ],
           ...
       }
       """

    satellites = []
    for name, line1, line2 in TLEs:
        name = name.strip()
        line1 = line1.strip()
        line2 = line2.strip()
        satellites.append((name, Satrec.twoline2rv(line1, line2)))

    startTime = datetime.now(timezone.utc)
    currentTime = startTime
    endTime = startTime + timedelta(hours=duration)
    dt = timedelta(seconds=step)

    propagated = {name: [] for name, _ in satellites}

    while currentTime < endTime:
        jd, fr = GetJulianDate(currentTime)

        for name, sat in satellites:
            e, r ,v = sat.sgp4(jd, fr)
            if e == 0:
                propagated[name].append({
                    "time": currentTime,
                    "r": r,  # position (km)
                    "v": v  # velocity (km/s)
                })
        currentTime += dt
        print(f"Propagating at time {currentTime}")

    return propagated
