from orbit.coverage_calculations import simulation_parameters, compute_coverage_grid, generate_grid
from orbit.HelperFucntions.PullTLEs import get_starlink_tles
from orbit.QuickPropagate import quickPropagate
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

def coverage_mapping():
    simulation_params = simulation_parameters()
    tle_data = get_starlink_tles()

    print("Propagating satellites...")
    propagated = quickPropagate(tle_data, simulation_params["simulation_duration_hours"], simulation_params["porpagation_time_step"])

    lats, lons, _ = generate_grid(simulation_params)
    coverage_grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"], metric="coverage_percent")
    capacity_grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"], metric="coverage_capacity")

    generate_heatmap(simulation_params, coverage_grid, title="Coverage Percentage Average Over Time")
    generate_heatmap(simulation_params, capacity_grid, title="Coverage Capacity Average Over Time")



def generate_heatmap(simulation_config, grid, title):
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

    vmax = np.max(grid)

    img = ax.imshow(
        grid,
        origin="lower",
        extent=[simulation_config["lon_min"], simulation_config["lon_max"],simulation_config["lat_min"], simulation_config["lat_max"]],
        cmap="viridis",
        vmin=0,
        vmax=vmax,
        transform=ccrs.PlateCarree(),
        alpha=0.75,
    )

    if "Coverage" in title:
        colorbar_label = "Coverage %"
    else:
        colorbar_label = "Capacity (mbps)"

    plt.colorbar(img, ax=ax, label=colorbar_label)
    plt.title(title)
    plt.tight_layout()
    plt.show()