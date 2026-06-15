import numpy as np
from multiprocessing.dummy import Pool
from os import cpu_count

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

def compute_point(args):
    lat, lon, propagated_satellites, metric = args
    coverage_point_stats = checkForCoverage(lat, lon, propagated_satellites)

    if metric == "coverage_percent":
        print(f"Checking {metric} at ({lat}, {lon})")
        return coverage_point_stats["coverage_percent"]
    elif metric == "coverage_capacity":
        print(f"Checking {metric} at ({lat}, {lon})")
        return coverage_point_stats["coverage_capacity"]



#Compute coverage for grid points
def compute_coverage_grid(lats, lons, propagated_data, metric = "coverage_percent"):

    tasks = [
        (lat, lon, propagated_data, metric)
        for lat in lats
        for lon in lons
    ]

    with Pool(cpu_count()) as pool:
        results = pool.map(compute_point, tasks)

    coverage_grid = np.array(results).reshape(len(lats), len(lons))


    return coverage_grid