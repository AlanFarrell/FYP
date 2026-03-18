import requests
import os


def get_starlink_tles():
    tle_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"

    try:
        response = requests.get(tle_url, timeout=8)
        response.raise_for_status()
        print("[INFO] Downloaded Starlink TLEs")
        return response.text.strip().split("\n")

    except Exception as e:
        print(f"[ERROR] TLE download failed: {e}. Using local backup...")

        here = os.path.dirname(os.path.abspath(__file__))
        tle_path = os.path.join(here, "starlink.tle")  # FIXED

        with open(tle_path, "r") as f:
            return f.read().strip().split("\n")