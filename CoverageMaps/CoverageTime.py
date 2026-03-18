import numpy as np
from orbit.VisibilityWindow import coverage_time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from orbit.HelperFucntions.PullTLEs import get_starlink_tles


def coverage_map():
    TLEdata = get_starlink_tles()

    lat_min, lat_max = 51.3, 56.0
    lon_min, lon_max = -10.7, -5.5
    step = 2

    lats = np.arange(lat_min, lat_max, step)
    lons = np.arange(lon_min, lon_max, step)

    grid = np.zeros((len(lats), len(lons)))


    print("Generating coverage map...")
    print(f"Grid size: {len(lats)} x {len(lons)} points")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            print(f"Checking coverage at {lat}, {lon}")
            result = coverage_time(obs_lat=lat, obs_lon=lon, lines=TLEdata, dtc_only =True, verbose=True)
            grid[i, j] = result["coverage_percent"]



    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    ax.coastlines(resolution="10m", color="black", linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)

    img = ax.imshow(
        grid,
        origin="lower",
        extent=[lon_min, lon_max, lat_min, lat_max],
        cmap="viridis",
        vmin=0, vmax=100,
        transform=ccrs.PlateCarree(),
        alpha=0.75
    )

    plt.colorbar(img, ax=ax, label="Coverage %")

    plt.title("Coverage Percentage Map Over Ireland")
    plt.tight_layout()
    plt.show()






