from sgp4.api import Satrec, jday
from datetime import datetime, timezone
from orbit.isVisible import is_visible
from orbit.BeamWidth import BeamFilter

def satellite_positions(when_utc=None, lines=None, obs_lat=None, obs_lon=None, verbose=True):

    beamwidthDeg = 30.0
    alt_m = 0.0

    visible_count = 0
    dtc_visible = 0


    if obs_lat is None or obs_lon is None:
        OBSERVER_SITES = [("Kells", 53.727508, -6.878310)]
        obs_name, obs_lat, obs_lon = OBSERVER_SITES[0]
    else:
        obs_name ="custom"

    unique_visible = {}



    #=====Finding  Julian date =====

    t = when_utc if when_utc is not None else datetime.now(timezone.utc)
    jd, fr = jday(t.year, t.month, t.day,
                  t.hour, t.minute, t.second + t.microsecond / 1e6)

    # ---- loop through all Starlink TLEs ----
    for i in range(0, len(lines) - 2, 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()

        satellite = Satrec.twoline2rv(line1, line2)
        e, r, v = satellite.sgp4(jd, fr)
        if e != 0:
            continue

    #=====Line of sight test  el >10 Degrees above horizon======
        ok, elev = is_visible(r, jd, fr, obs_lat, obs_lon, alt_m)
        if not ok:
            continue

        visible_count += 1

        unique_visible[name] = {
            "name": name,
            "position_km": r,
            "velocity": v,
            "error": e
        }

    satellite_positions = list(unique_visible.values())

    #=====Apply beamwidth filter =====
    filtered, best = BeamFilter(satellite_positions, jd, fr, obs_lat, obs_lon, alt_m,beamwidthDeg)


   #DTC count
    for name in unique_visible:
        if "DTC" in name:
            dtc_visible += 1

    if filtered:
        print("[summary] Satellites with viable Beamwidth (at a time instant):")
        for s in sorted(filtered, key=lambda item: item["name"]):
            print("  -", s["name"])


    print(f"Checking at lat lon: {obs_lat}, {obs_lon}")
    print(f"Total visible DTC (LoS only): {dtc_visible}")
    print(f"Total in-beam: {len(filtered)}")
    print(f"Optimal Satellite: {best}")
    print(" ")

    return filtered, best