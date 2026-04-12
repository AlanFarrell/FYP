import os
import requests
from orbit.HelperFucntions.DTCfilter import is_DTC


TLE_SOURCES = {
    "Starlink (All)": {
        "type": "online",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle",
        "local": "TLE_data/starlink.tle",
        "dtc_only": False
    },
    "Starlink (DTC Only)": {
        "type": "online",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle",
        "local": "TLE_data/starlink.tle",
        "dtc_only": True
    },
    "OneWeb": {
        "type": "online",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=2le",
        "local": "TLE_data/OneWeb.tle"
    },
    "Kuiper": {
        "type": "online",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=kuiper&FORMAT=tle",
        "local": "TLE_data/Kuiper.tle"
    }
}


def Pull_TLE_data(source):
    try:
        if source.get("type") == "online":
            response = requests.get(source["url"], timeout=8)
            response.raise_for_status()
            lines = response.text.strip().splitlines()
        else:
            raise Exception
    except Exception:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "..", source["local"])
        with open(path, "r") as f:
            lines = f.read().strip().splitlines()

    return lines


def parse_tles(lines, dtc_only=False):
    tles = []
    i = 0

    while i < len(lines) - 1:

        # Case 1: bare 2-line TLE
        if lines[i].startswith("1 ") and lines[i + 1].startswith("2 "):
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip()
            name = f"SAT-{line1[2:7]}"
            i += 2
        else:
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            i += 3

        norad_id = int(line1[2:7])

        if dtc_only and not is_DTC(norad_id):
            continue

        tles.append((name, line1, line2))

    return tles


def get_tles(constellation_name):
    if constellation_name not in TLE_SOURCES:
        raise ValueError(f"Unknown constellation: {constellation_name}")

    source = TLE_SOURCES[constellation_name]
    lines = Pull_TLE_data(source)
    return parse_tles(lines, dtc_only=source.get("dtc_only", False))
