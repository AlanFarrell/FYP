from sgp4.api import Satrec, jday
from datetime import datetime, timezone, time
import requests
import logging
import time as pytime
from logging.handlers import RotatingFileHandler
from orbit.isVisible import is_visible



handler = RotatingFileHandler(
    "satellite_stream.log",
    maxBytes=10_000_000,  # 10 MB
    backupCount=3         # keep 3 rotated files
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler("satellite_stream.log", mode="a"),
              logging.StreamHandler()]
)
log = logging.getLogger("satellite")



def satellite_positions(duration_s = 2):
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    response = requests.get(url)
    lines = response.text.strip().split("\n")

    visible_count = 0

    OBSERVER_SITES = [
        ("Kells", 53.727508, -6.878310)
    ]


    satellite_positions = []
    visible_sats = []
    obs_name, obs_lat, obs_lon = OBSERVER_SITES[0]

    start = pytime.time()
    while pytime.time() - start < duration_s:

        now = datetime.now(timezone.utc)
        jd, fr = jday(
            now.year, now.month, now.day,
            now.hour, now.minute, now.second + now.microsecond / 1e6
        )

        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()
            satellite = Satrec.twoline2rv(line1, line2)
            e, r, v = satellite.sgp4(jd, fr)

            ok, elev = is_visible(r, jd, fr, obs_lat, obs_lon)  # TEMP: 0° mask
            if not ok:
                continue
            visible_count += 1
            entry = {
                "name": name,
                "position_km": r,
                "velocity": v,
                "error": e
                }



            log.info(entry)
            satellite_positions.append(entry)

    print(f"[summary] visible={visible_count}, returned={len(satellite_positions)}")
    return satellite_positions