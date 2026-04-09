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
    tle_data = get_starlink_tles(dtc_only=True)
    print("Propagating satellites...")
    propagated = quickPropagate(tle_data, simulation_params["simulation_duration_hours"], simulation_params["porpagation_time_step"])
    lats, lons, _ = generate_grid(simulation_params)
    coverage_grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"], metric="coverage_percent")
    capacity_grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"], metric="coverage_capacity")
    generate_heatmap(simulation_params, coverage_grid, title="Coverage Percentage Average Over Time", colourBarLabel="Coverage Time as percent")
    generate_heatmap(simulation_params, capacity_grid, title="Coverage Capacity Average Over Time", colourBarLabel="Capacity (Mbps)")


def generate_heatmap(simulation_config, grid, title, colourBarLabel=None):
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

    vmin = np.nanmin(grid)
    vmax = np.nanmax(grid)

    img = ax.imshow(
        grid,
        origin="lower",
        extent=[
            simulation_config["lon_min"], simulation_config["lon_max"],
            simulation_config["lat_min"], simulation_config["lat_max"]
        ],
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
        transform=ccrs.PlateCarree(),
        alpha=0.75,
    )

    #if contours were [0,0,0,0] system would crash -> this block solves this issue
    if vmin == vmax or np.isnan(vmin) or np.isnan(vmax):
        contour_levels = None
    else:
        contour_levels = np.linspace(vmin, vmax, 10)
    #----------------------------------------------------------------------------

    if contour_levels is not None:
        cs = ax.contour(
            grid,
            levels=contour_levels,
            colors='black',
            linewidths=0.5,
            origin="lower",
            extent=[
                simulation_config["lon_min"], simulation_config["lon_max"],
                simulation_config["lat_min"], simulation_config["lat_max"]
            ],
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