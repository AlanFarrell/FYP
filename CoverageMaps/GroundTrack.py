import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from orbit.QuickPropagate import quickPropagate
from orbit.HelperFucntions.TLELoader import get_tles
from orbit.HelperFucntions.GeodeticToECEF import ecef_to_latlon
from config import TLEoption


def plot_ground_tracks():
    tle_choice = "Kuiper"

    print("[INFO] Loading TLEs")
    TLEs = get_tles(tle_choice)
    print("[INFO] Propagating satellites")
    propagated_satellites = quickPropagate(TLEs)

    figure = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines(resolution="110m")
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)

    axins = plt.axes([0.55, 0.05, 0.5, 0.6], projection=ccrs.PlateCarree())
    axins.set_extent([-12, -5, 50, 56])
    axins.coastlines(resolution="10m")
    axins.add_feature(cfeature.LAND, facecolor="lightgray")
    axins.add_feature(cfeature.OCEAN)

    ax.plot(
        [-12, -5, -5, -12, -12],
              [50, 50, 56, 56, 50],
              color='black',
              linewidth=2,
              transform=ccrs.PlateCarree()
)


    for satellite_name in list(propagated_satellites.keys())[:]:
        lats, lons = [], []

        for entry in propagated_satellites[satellite_name]:
            timestamp, x, y, z = entry
            r_ecef = (x, y, z)
            lat, lon = ecef_to_latlon(r_ecef)
            lats.append(lat)
            lons.append(lon)

        ax.plot(lons, lats, linewidth=1, transform=ccrs.Geodetic())
        axins.plot(lons, lats, linewidth=1, transform=ccrs.Geodetic())

    plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.05)
    plt.show()
