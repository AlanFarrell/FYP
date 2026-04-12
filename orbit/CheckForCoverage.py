from typing import Any
import numpy as np
from numpy import floating

from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.isVisible import visibility_check
from orbit.BeamWidth import BeamFilter
from LinkBudgetCalculations.ComputeLinkBudget import compute_link_budget

_visibility_cache = {}
"""
Optimisations:
Satellite visibility is precomputed once per timestep instead of being recomputed
  for every grid point and every timestep.
  
The satellite visibility calculations are cached and reused across calls.

When a timestep index (idx) is provided, only that timestep is computed now

Removes the original grid × time × satellite nested loop to reduces runtime 

Satellite geometry is handled once per timestep
"""

def precompute_data(propagated_satellites, lat, lon, timestep_indices=None):
    visibility_at_time = []

    full_timeline = next(iter(propagated_satellites.values()))
    if timestep_indices is None:
        timestep_indices = range(len(full_timeline))

    for tidx in timestep_indices:
        t = full_timeline[tidx]["time"]
        jd, fr = GetJulianDate(t)

        visible_satellites = []
        for satellite_name, samples in propagated_satellites.items():
            if tidx >= len(samples):
                continue

            r_teme = samples[tidx]["r"]
            ok, elevation = visibility_check(r_teme, jd, fr, lat, lon)
            if not ok:
                continue

            visible_satellites.append({
                "name": satellite_name,
                "position_km": r_teme,
                "elevation_degrees": elevation
            })

        visibility_at_time.append((t, jd, fr, visible_satellites))

    return visibility_at_time


def checkForCoverage(lat, lon, propagatedSatellites, simulation_duration, beamwidth=15.0, idx=None):
    timestep_capacities = []
    coverage_windows = []
    in_coverage = False
    window_start = None

    #===============================================
    cache_key = (lat, lon, idx)

    if cache_key in _visibility_cache:
        visibility_by_time = _visibility_cache[cache_key]
    else:
        if idx is not None:
            visibility_by_time = precompute_data(propagatedSatellites, lat, lon, timestep_indices=[idx])
        else:
            visibility_by_time = precompute_data(propagatedSatellites, lat, lon)

        _visibility_cache[cache_key] = visibility_by_time

    for t, jd, fr, visible_satellites in visibility_by_time:
        filtered_satellites, optimal_satellite = BeamFilter(visible_satellites, jd, fr, lat, lon, obs_alt=0.0, beamwidth_deg=beamwidth)
        coverage_available = len(filtered_satellites) > 0

        if coverage_available:
            link_budget = compute_link_budget(optimal_satellite, filtered_satellites, jd, fr, lat, lon)
            timestep_capacities.append(link_budget["capacity_mbps"])
        else:
            timestep_capacities.append(0.0)

        if coverage_available and not in_coverage:
            in_coverage = True
            window_start = t

        if not coverage_available and in_coverage:
            in_coverage = False
            coverage_windows.append((window_start, t))

    # ============================================================================

    if in_coverage and window_start:
        coverage_windows.append((window_start, visibility_by_time[-1][0]))

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