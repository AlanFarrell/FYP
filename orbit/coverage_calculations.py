import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from orbit.CheckForCoverage import checkForCoverage


def simulation_parameters():
    from config import SimulationConfig
    return {
        "lat_min": SimulationConfig.LAT_MIN,
        "lat_max": SimulationConfig.LAT_MAX,
        "lon_min": SimulationConfig.LON_MIN,
        "lon_max": SimulationConfig.LON_MAX,
        "lat_lon_step": SimulationConfig.LAT_LON_STEP,
        "propagation_time_step": SimulationConfig.PROPAGATION_TIME_STEP,
        "simulation_duration_hours": SimulationConfig.SIMULATION_DURATION_HOURS,
    }

#Make latitude/longitude grid
def generate_grid(grid_paramaters):
    lats = np.arange(grid_paramaters["lat_min"], grid_paramaters["lat_max"], grid_paramaters["lat_lon_step"])
    lons = np.arange(grid_paramaters["lon_min"], grid_paramaters["lon_max"], grid_paramaters["lat_lon_step"])
    grid = np.zeros((len(lats), len(lons)))
    return lats, lons, grid


#Compute coverage for grid points
def compute_coverage_grid(lats, lons, propagated_data, simulation_duration, metric = "coverage_percent"):
    coverage_grid = np.zeros((len(lats), len(lons)))

    print(f"Computing coverage for {metric}")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):

            coverage_statistic = checkForCoverage(lat, lon, propagated_data, simulation_duration, beamwidth=15)

            if metric == "coverage_percent":
                print(f"Checking {metric} at ({lat}, {lon})")
                coverage_grid[i, j] = coverage_statistic["coverage_percent"]
            elif metric == "coverage_capacity":
                print(f"Checking {metric} at ({lat}, {lon})")
                coverage_grid[i, j] = coverage_statistic["coverage_capacity"]
            else:
                raise ValueError("Unknown Metric")

    return coverage_grid