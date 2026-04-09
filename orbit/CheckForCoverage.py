from typing import Any
import numpy as np
from numpy import floating

from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.isVisible import is_visible
from orbit.BeamWidth import BeamFilter
from LinkBudgetCalculations.ComputeLinkBudget import compute_link_budget

def checkForCoverage(lat, lon, propagatedSatellites, simulation_duration, beamwidth=15.0, idx=None):
    timestep_capacities = []
    coverage_windows = []
    in_coverage = False
    window_start = None

    if idx is not None:
        timeline = [next(iter(propagatedSatellites.values()))[idx]["time"]]
    else:
        timeline = [entry["time"] for entry in next(iter(propagatedSatellites.values()))]

    for tidx, t in enumerate(timeline):
        actual_idx = idx if idx is not None else tidx

        jd, fr = GetJulianDate(t)
        visible_satellites = []
        for satellite_name, samples in propagatedSatellites.items():
            if actual_idx >= len(samples):
                continue
            sat_data = samples[actual_idx]
            r_teme = sat_data["r"]

            ok, elevation = is_visible(r_teme, jd, fr, lat, lon)
            if not ok:
                continue

            visible_satellites.append({
                "name": satellite_name,
                "position_km": r_teme,
                "elevation_degrees": elevation
            })

        filtered_satellites, optimal_satellite = BeamFilter(visible_satellites, jd, fr, lat, lon, obs_alt=0.0, beamwidth_deg=beamwidth)
        link_budget = compute_link_budget(optimal_satellite, filtered_satellites, jd, fr, lat, lon)
        timestep_capacities.append(link_budget["capacity_mbps"])

        coverage_available = len(filtered_satellites) > 0

        if coverage_available and not in_coverage:
            in_coverage = True
            window_start = t

        if not coverage_available and in_coverage:
            in_coverage = False
            coverage_windows.append((window_start, t))

    if in_coverage and window_start:
        coverage_windows.append((window_start, timeline[-1]))

    average_capacity, coverage_percent, total_mins = Compute_statistic(coverage_windows, simulation_duration, timestep_capacities)

    return {
        "coverage_windows": coverage_windows,
        "total_minutes": total_mins,
        "coverage_percent": coverage_percent,
        "coverage_capacity": average_capacity,
    }


def Compute_statistic(coverage_windows: list[Any], simulation_duration, timestep_capacities: list[Any]) -> tuple[
    float, float | Any, floating[Any] | float]:
    total_secs = sum((end - start).total_seconds() for start, end in coverage_windows)
    coverage_percent = (total_secs / (simulation_duration * 3600)) * 100.0
    total_mins = total_secs / 60.0
    average_capacity = np.mean(timestep_capacities) if timestep_capacities else 0.0
    return average_capacity, coverage_percent, total_mins