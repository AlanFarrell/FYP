from orbit.coverage_calculations import simulation_parameters, compute_coverage_grid, generate_grid
from orbit.QuickPropagate import quickPropagate
from orbit.HelperFucntions.TLELoader import get_tles

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from scipy.ndimage import gaussian_filter

def coverage_mapping():

    #tle_choice = "Starlink (DTC Only)"
    tle_choice = "Starlink (All)"
    #tle_choice = "OneWeb"
    #tle_choice = "Kuiper"

    print(f"[INFO] Loading TLEs for {tle_choice}")
    simulation_params = simulation_parameters(lat_lon_step=0.1)
    tle_data = get_tles(tle_choice)

    print("Propagating satellites...")
    propagated = quickPropagate(tle_data, simulation_params["simulation_duration_hours"], simulation_params["propagation_time_step"])
    lats, lons, _ = generate_grid(simulation_params)
    coverage_grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"], metric="coverage_percent")
    capacity_grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"], metric="coverage_capacity")
    generate_heatmap(simulation_params, coverage_grid, title="Coverage Percentage Average Over Time", colourBarLabel="Coverage Time as percent")
    generate_heatmap(simulation_params, capacity_grid, title="Coverage Capacity Average Over Time", colourBarLabel="Capacity (Mbps)")


def generate_heatmap(simulation_config, grid, title, colourBarLabel=None):
    grid = gaussian_filter(grid, sigma=1.0)
    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([
        simulation_config["lon_min"], simulation_config["lon_max"],
        simulation_config["lat_min"], simulation_config["lat_max"]
    ])

    ax.coastlines(resolution="10m", linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="black")

    vmin = np.percentile(grid, 5)
    vmax = np.percentile(grid, 95)

    lon = np.linspace(simulation_config["lon_min"], simulation_config["lon_max"], grid.shape[1])
    lat = np.linspace(simulation_config["lat_min"], simulation_config["lat_max"], grid.shape[0])
    Lon, Lat = np.meshgrid(lon, lat)

    img = ax.pcolormesh(
        Lon, Lat, grid,
        cmap="plasma",
        vmin=vmin,
        vmax=vmax,
        shading="nearest",
        transform=ccrs.PlateCarree()
    )

    #if contours were [0,0,0,0] system would crash -> this block solves this issue
    if vmin == vmax or np.isnan(vmin) or np.isnan(vmax):
        contour_levels = None
    else:
        contour_levels = np.linspace(vmin, vmax, 6)
    #----------------------------------------------------------------------------

    if contour_levels is not None:
        cs = ax.contour(
            Lon, Lat, grid,
            levels=contour_levels,
            colors='black',
            linewidths=0.4,
            alpha=0.6,
            transform=ccrs.PlateCarree()
        )

        ax.clabel(cs, inline=True, fontsize=6, fmt="%.1f")

    # Stats
    mean_val = np.mean(grid)
    min_val = np.min(grid)
    max_val = np.max(grid)

    stats_text = (f"Max:  {max_val:.2f}\n"
                  f"Min:  {min_val:.2f}\n"
                  f"Mean: {mean_val:.2f}")

    plt.gcf().text(
        0.82, 0.25,
        stats_text,
        fontsize=10,
        bbox=dict(facecolor='white', alpha=0.8)
    )

    plt.colorbar(img, ax=ax, label=colourBarLabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()