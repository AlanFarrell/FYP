
from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef
from orbit.QuickPropagate import quickPropagate
from orbit.HelperFucntions.TLELoader import get_tles
from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.HelperFucntions.GeodeticToECEF import ecef_to_latlon


def plot_ground_tracks():
    tle_choice = "Starlink (DTC Only)"
    #tle_choice = "Starlink (All)"
    #tle_choice = "OneWeb"
    #tle_choice = "Kuiper"

    start_time = datetime(2026, 4, 23, 7, 0, tzinfo=timezone.utc)
    simulation_duration_hours = 4
    step_seconds =  30

    print("[INFO] Loading TLEs")
    tles = get_tles(tle_choice)
    print("[INFO] Propagating satellites")
    propagated_satellites = quickPropagate(tles, simulation_duration_hours, step_seconds, start_time)

    figure = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines(resolution="110m")
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)

    for satellite_name in list(propagated_satellites.keys())[:200]:
        lats, lons = [], []

        for entry in propagated_satellites[satellite_name]:
            jd, fr = GetJulianDate(entry["time"])
            r_teme = entry["r"]
            r_ecef = teme_to_ecef(r_teme, jd, fr)
            lat, lon = ecef_to_latlon(r_ecef)

            lats.append(lat)
            lons.append(lon)


        ax.plot(lons, lats, linewidth=1, transform=ccrs.Geodetic())
    plt.title(f"OneWeb Ground Tracks")
    plt.tight_layout()
    plt.show()
