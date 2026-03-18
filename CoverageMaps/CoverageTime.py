import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from orbit.HelperFucntions.PullTLEs import get_starlink_tles
from orbit.CheckForCoverage import checkForCoverage
from orbit.QuickPropagate import quickPropagate

def coverage_map():
    lat_min, lat_max = 51.3, 56.0
    lon_min, lon_max = -10.7, -5.5
    TimeStep = 60
    LatLonStep = 1
    TLEdata = get_starlink_tles()
    propagated_data = quickPropagate(TLEdata, 3, TimeStep, use_dtc_only=True)

    lats = np.arange(lat_min, lat_max, LatLonStep)
    lons = np.arange(lon_min, lon_max, LatLonStep)

    grid = np.zeros((len(lats), len(lons)))

    print("Generating coverage map...")
    print(f"Grid size: {len(lats)} x {len(lons)} points")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            print(f"Checking coverage at {lat}, {lon}")
            stats = checkForCoverage(lat, lon, propagated_data)
            grid[i, j] = stats["coverage_percent"]




    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max])

    ax.coastlines(resolution="10m", linewidth=1)
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
        alpha=0.75,
    )

    plt.colorbar(img, ax=ax, label="Coverage %")
    plt.title("24‑Hour Starlink Coverage Map Over Ireland")
    plt.tight_layout()
    plt.show()






