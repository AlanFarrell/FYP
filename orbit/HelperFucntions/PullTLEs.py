import requests
import os
from orbit.HelperFucntions.DTCfilter import is_DTC


def get_starlink_tles(dtc_only=False):
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    tles = []

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        print("[INFO] Downloaded Starlink TLEs")
        lines = response.text.strip().split("\n")
    except Exception as e:
        print(f"[ERROR] TLE download failed: {e}. Using local backup...")
        here = os.path.dirname(os.path.abspath(__file__))
        tle_path = os.path.join(here, "../TLE_data/starlink.tle")

        with open(tle_path, "r") as f:
            lines = f.read().strip().split("\n")


    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i+1].strip()
        line2 = lines[i+2].strip()

        norad_id = int(line1[2:7])

        if dtc_only:
            if is_DTC(norad_id):
                tles.append((name, line1, line2))
        else:
            tles.append((name, line1, line2))

    return tles