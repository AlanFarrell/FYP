from sgp4.api import Satrec, jday
from datetime import datetime, timezone
import requests
from orbit.isVisible import is_visible


def satellite_positions():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    response = requests.get(url)
    lines = response.text.strip().split("\n")
    alt_m = 0.0
    visible_count = 0

    OBSERVER_SITES = [
        ("Kells", 53.727508, -6.878310)
    ]

    unique_visible = {}
    obs_name, obs_lat, obs_lon = OBSERVER_SITES[0]

    now = datetime.now(timezone.utc)
    jd, fr = jday(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second + now.microsecond / 1e6
    )

    # ---- loop through all Starlink TLEs ----
    for i in range(0, len(lines) - 2, 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()

        satellite = Satrec.twoline2rv(line1, line2)
        e, r, v = satellite.sgp4(jd, fr)
        if e != 0:
            continue

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


    if unique_visible:
        print("[summary] Visible satellites:")
        for s in sorted(unique_visible):
            print(f"  - {s}")

    print(f"Total visible: {len(unique_visible)} (raw hits: {visible_count})")

    return satellite_positions