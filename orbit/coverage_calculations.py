import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from orbit.CheckForCoverage import checkForCoverage
from config import SimulationConfig

#Make latitude/longitude grid
def generate_grid():
    lats = np.arange(SimulationConfig.LAT_MIN, SimulationConfig.LAT_MAX, SimulationConfig.LAT_LON_STEP)
    lons = np.arange(SimulationConfig.LON_MIN, SimulationConfig.LON_MAX, SimulationConfig.LAT_LON_STEP)
    grid = np.zeros((len(lats), len(lons)))
    return lats, lons, grid


#Compute coverage for grid points
def compute_coverage_grid(lats, lons, propagated_data, metric = "coverage_percent"):
    coverage_grid = np.zeros((len(lats), len(lons)))

    print(f"Computing coverage for {metric}")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):

            coverage_statistic = checkForCoverage(lat, lon, propagated_data)

            if metric == "coverage_percent":
                print(f"Checking {metric} at ({lat}, {lon})")
                coverage_grid[i, j] = coverage_statistic["coverage_percent"]
            elif metric == "coverage_capacity":
                print(f"Checking {metric} at ({lat}, {lon})")
                coverage_grid[i, j] = coverage_statistic["coverage_capacity"]
            else:
                raise ValueError("Unknown Metric")

    return coverage_grid