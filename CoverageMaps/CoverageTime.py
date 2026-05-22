from orbit.coverage_calculations import compute_coverage_grid, generate_grid
from orbit.QuickPropagate import quickPropagate
from orbit.HelperFucntions.TLELoader import get_tles
from CoverageMaps.GenerateHeatMap import generate_heatmap
from config import TLEoption, SimulationConfig

def coverage_mapping():
    tle_choice = TLEoption.tle_choice

    print(f"[INFO] Loading TLEs for {tle_choice}")
    tle_data = get_tles(tle_choice)
    print("Propagating satellites...")

    propagated_satellites = quickPropagate(tle_data)
    lats, lons, _ = generate_grid()

    coverage_grid = compute_coverage_grid(lats, lons, propagated_satellites, metric="coverage_percent")
    capacity_grid = compute_coverage_grid(lats, lons, propagated_satellites, metric="coverage_capacity")

    generate_heatmap(coverage_grid, title="Coverage Percentage Average Over Time", colourBarLabel="Coverage Time as percent")
    generate_heatmap(capacity_grid, title="Coverage Capacity Average Over Time", colourBarLabel="Capacity (Mbps)")
