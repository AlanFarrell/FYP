import numpy as np
from orbit.VisibilityWindow import coverage_time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import requests
import os




def coverage_map():
    tle_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    try:
        response = requests.get(tle_url, timeout=8)
        response.raise_for_status()
        lines = response.text.strip().split("\n")
    except Exception as e:
        print(f"[Error]: TLE download failed: {e}, using local backup ")
        here = os.path.dirname(os.path.abspath(__file__))   # <-- path to /orbit
        tle_path = os.path.join(here, "..", "orbit", "starlink.tle")
        with open(tle_path, "r") as f:
            lines = f.read().strip().split("\n")





    lat_min, lat_max = 51.3, 56.0
    lon_min, lon_max = -10.7, -5.5
    lat_step, lon_step = 0.1, 0.1

    lats = np.arange(lat_min, lat_max, lat_step)
    lons = np.arange(lon_min, lon_max, lon_step)

    grid = np.zeros((len(lats), len(lons)))


    print("Generating coverage map...")
    print(f"Grid size: {len(lats)} x {len(lons)} points")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            print(f"Checking coverage at {lat}, {lon}")
            result = coverage_time(obs_lat=lat, obs_lon=lon, lines=lines)
            grid[i, j] = result["coverage_percent"]

    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())


    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # Add map features
    ax.coastlines(resolution="10m", color="black", linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)

    # Plot the coverage grid ON the map
    img = ax.imshow(
        grid,
        origin="lower",
        extent=[lon_min, lon_max, lat_min, lat_max],
        cmap="viridis",
        vmin=0, vmax=100,
        transform=ccrs.PlateCarree(),
        alpha=0.75
    )

    # Colorbar
    plt.colorbar(img, ax=ax, label="Coverage %")

    plt.title("Coverage Percentage Map Over Ireland")
    plt.tight_layout()
    plt.show()






