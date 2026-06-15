from datetime import datetime

from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.isVisible import visibility_check
from orbit.BeamWidth import BeamFilter
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from LinkBudgetCalculations.ComputeLinkBudget import compute_link_budget
from config import SimulationConfig


def precompute_data(propagated_satellites, lat, lon, timestep_indices=None):
    visibility_at_time = []
    g_ecef = LatLonToECEF(lat, lon)

    full_timeline = next(iter(propagated_satellites.values()))
    if timestep_indices is None:
        timestep_indices = range(len(full_timeline))

    satellite_items = list(propagated_satellites.items())
    for time_index in timestep_indices:
        entry = full_timeline[time_index]
        timestamp, x , y, z = entry
        t = datetime.fromtimestamp(timestamp)
        visible_satellites = []

        for satellite_name, samples in satellite_items:
            if time_index >= len(samples):
                continue

            entry = samples[time_index]
            _, x, y, z = entry
            r_ecef = (x, y, z)


            ok, elevation = visibility_check(r_ecef, g_ecef, lat, lon)
            if not ok:
                continue

            visible_satellites.append({
                "name": satellite_name,
                "position_km": r_ecef,
                "elevation_degrees": elevation
            })

        visibility_at_time.append((t, visible_satellites))
    return visibility_at_time


def checkForCoverage(lat, lon, propagatedSatellites, time_step_index=None):
    coverage_capacity_sum = 0.0
    coverage_capacity_count = 0
    coverage_windows = []
    in_coverage = False
    window_start_time = None

    visibility_by_time = (precompute_data(propagatedSatellites, lat, lon, timestep_indices=[time_step_index])
        if time_step_index is not None
        else precompute_data(propagatedSatellites, lat, lon)
    )

    for t, visible_satellites in visibility_by_time:
        jd, fr = GetJulianDate(t)

        if visible_satellites:
            filtered, optimal = BeamFilter(visible_satellites, lat, lon, obs_alt=0.0)
        else:
            filtered = False

        if filtered:
            link = compute_link_budget(optimal, filtered, jd, fr, lat, lon)
            capacity_this_step = link["capacity_mbps"]
            coverage_capacity_sum += capacity_this_step
            coverage_capacity_count += 1

            if not in_coverage:
                in_coverage = True
                window_start_time = t
        else:
            if in_coverage:
                in_coverage = False
                coverage_windows.append((window_start_time, t))

    if in_coverage and window_start_time is not None:
        coverage_windows.append((window_start_time, visibility_by_time[-1][0]))

    total_seconds = sum((end - start).total_seconds()for start, end in coverage_windows)
    coverage_percent = (total_seconds / (SimulationConfig.SIMULATION_DURATION_HOURS * 3600.0)) * 100.0
    average_capacity = (coverage_capacity_sum / coverage_capacity_count if coverage_capacity_count > 0 else 0.0)

    return {
        "coverage_percent": coverage_percent,
        "coverage_capacity": average_capacity,
    }