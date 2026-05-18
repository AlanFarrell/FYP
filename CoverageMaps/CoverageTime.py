from orbit.coverage_calculations import simulation_parameters, compute_coverage_grid, generate_grid
from orbit.QuickPropagate import quickPropagate
from orbit.HelperFucntions.TLELoader import get_tles
from CoverageMaps.GenerateHeatMap import generate_heatmap
from config import TLEoption

from datetime import datetime, timezone
import matplotlib
matplotlib.use("TkAgg")

def coverage_mapping():
    tle_choice = TLEoption.tle_choice

    print(f"[INFO] Loading TLEs for {tle_choice}")
    simulation_params = simulation_parameters()
    tle_data = get_tles(tle_choice)

    print("Propagating satellites...")

    start_time = datetime(year=2026, month=4, day=23, hour=7, minute=0, second=0, tzinfo=timezone.utc)

    propagated_satellites = quickPropagate(tle_data, simulation_params["simulation_duration_hours"], simulation_params["propagation_time_step"], start_time_utc=start_time)
    lats, lons, _ = generate_grid(simulation_params)

    coverage_grid = compute_coverage_grid(lats, lons, propagated_satellites, simulation_params["simulation_duration_hours"], metric="coverage_percent")
    capacity_grid = compute_coverage_grid(lats, lons, propagated_satellites, simulation_params["simulation_duration_hours"], metric="coverage_capacity")

    generate_heatmap(simulation_params, coverage_grid, title="Coverage Percentage Average Over Time", colourBarLabel="Coverage Time as percent")
    generate_heatmap(simulation_params, capacity_grid, title="Coverage Capacity Average Over Time", colourBarLabel="Capacity (Mbps)")
