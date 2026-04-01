import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from orbit.CheckForCoverage import checkForCoverage



#Generate config
def simulation_parameters():
    return {
        "lat_min": 51.3,
        "lat_max": 56.0,
        "lon_min": -10.7,
        "lon_max": -5.5,
        "lat_lon_step": 1,
        "porpagation_time_step": 30,
        "simulation_duration_hours": 3
    }


#Make latitude/longitude grid
def generate_grid(grid_paramaters):
    lats = np.arange(grid_paramaters["lat_min"], grid_paramaters["lat_max"], grid_paramaters["lat_lon_step"])
    lons = np.arange(grid_paramaters["lon_min"], grid_paramaters["lon_max"], grid_paramaters["lat_lon_step"])
    grid = np.zeros((len(lats), len(lons)))
    return lats, lons, grid


#Compute coverage for grid points
def compute_coverage_grid(lats, lons, propagated_data, simulation_duration, metric = "coverage_percent"):
    grid = np.zeros((len(lats), len(lons)))

    print(f"Computing coverage for {metric}")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            print(f"Checking coverage at ({lat}, {lon})")
            stats = checkForCoverage(lat, lon, propagated_data, simulation_duration)

            if metric == "coverage_percent":
                grid[i, j] = stats["coverage_percent"]
            elif metric == "coverage_capacity":
                grid[i, j] = stats["coverage_capacity"]
            else:
                raise ValueError("Unknown Metric")

    return grid



