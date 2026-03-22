import requests
import os
from orbit.HelperFucntions.DTCfilter import is_DTC

def get_starlink_tles(dtc_only=False):
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        print("[INFO] Downloaded Starlink TLEs")
        lines = response.text.strip().split("\n")
    except Exception as e:
        print(f"[ERROR] TLE download failed: {e}. Using local backup...")
        here = os.path.dirname(os.path.abspath(__file__))
        tle_path = os.path.join(here, "starlink.tle")

        with open(tle_path, "r") as f:
            lines = f.read().strip().split("\n")

    if not dtc_only:
        return lines

    # ---- Apply DTC filter ----
    # filtered_satellites = []
    #
    # for i in range(0, len(lines), 3):
    #     fields = lines.split()
    #     norad_id = int(fields[1][:5])
    #
    #     if is_DTC(norad_id):
    #         filtered_satellites.extend(lines[i:i+3])
    #
    # print(f"[INFO] DTC filter: kept {len(filtered_satellites)//3} satellites")
    # return filtered_satellites

