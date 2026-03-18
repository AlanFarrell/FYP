from sgp4.api import Satrec, jday
from datetime import datetime, timezone
from orbit.isVisible import is_visible
from orbit.BeamWidth import BeamFilter

def satellite_positions(
                        when_utc=None,
                        lines=None,
                        obs_lat=None,
                        obs_lon=None,
                        verbose=True):

    beamwidthDeg = 30.0
    altitude_m = 0.0
    dtc_visible_count = 0

    #=====Finding  Julian date =====
    jd, fr = jday(
        when_utc.year,
        when_utc.month,
        when_utc.day,
        when_utc.hour,
        when_utc.minute,
        when_utc.second + when_utc.microsecond / 1e6
    )

    visible_satellites, dtc_visible = propagate_visible_satellites(
        lines, jd, fr, obs_lat, obs_lon
    )

    filtered_satellites, optimal_satellites = BeamFilter(
        visible_satellites,
        jd,
        fr,
        obs_lat,
        obs_lon,
        altitude_m,
        beamwidthDeg
    )

    if verbose:
        print("[summary] Satellites with viable Beamwidth (at a time instant):")
        for s in sorted(filtered_satellites, key=lambda item: item["name"]):
            print("  -", s["name"])

    if verbose:
        print(f"Checking at lat lon: {obs_lat}, {obs_lon}")
        print(f"Total visible DTC (LoS only): {dtc_visible_count}")
        print(f"Total in-beam: {len(filtered_satellites)}")
        print(f"Optimal Satellite: {optimal_satellites}")
        print(" ")

    return filtered_satellites, optimal_satellites





def propagate_visible_satellites(lines, jd, fr, obs_lat, obs_lon, observer_alt=0.0):
    visible = []
    dtc_count = 0

    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()

        sat = Satrec.twoline2rv(line1, line2)
        e, r, v = sat.sgp4(jd, fr)
        if e != 0:
            continue

        ok, elev_deg = is_visible(r, jd, fr, obs_lat, obs_lon, observer_alt)
        if not ok:
            continue

        if "DTC" in name.upper():
            dtc_count += 1

        visible.append({
            "name": name,
            "position_km": r,
            "velocity_km_s": v,
            "elevation_deg": elev_deg,
        })

    return visible, dtc_count