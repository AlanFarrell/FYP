from orbit.coverage_calculations import simulation_parameters, compute_coverage_grid, generate_grid
from orbit.HelperFucntions.PullTLEs import get_starlink_tles
from orbit.QuickPropagate import quickPropagate
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def coverage_mapping():
    simulation_params = simulation_parameters()
    tle_data = get_starlink_tles()

    print("Propagating satellites...")
    propagated = quickPropagate(tle_data, simulation_params["simulation_duration_hours"], simulation_params["porpagation_time_step"])

    lats, lons, _ = generate_grid(simulation_params)
    grid = compute_coverage_grid(lats, lons, propagated, simulation_params["simulation_duration_hours"])
    generate_coverage_heatmap(simulation_params, grid)


def generate_coverage_heatmap(simulation_config, grid):
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

    img = ax.imshow(
        grid,
        origin="lower",
        extent=[simulation_config["lon_min"], simulation_config['lon_max'], simulation_config["lat_min"], simulation_config["lat_max"]],
        cmap="viridis",
        vmin=0,
        vmax=100,
        transform=ccrs.PlateCarree(),
        alpha=0.75,
    )

    plt.colorbar(img, ax=ax, label="Coverage %")
    plt.title("Starlink Coverage Map Over Ireland")
    plt.tight_layout()
    plt.show()