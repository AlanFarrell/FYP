import numpy as np
from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.isVisible import visibility_check
from orbit.BeamWidth import BeamFilter
from LinkBudgetCalculations.ComputeLinkBudget import compute_link_budget


def precompute_data(propagated_satellites, lat, lon, timestep_indices=None):
    visibility_at_time = []

    full_timeline = next(iter(propagated_satellites.values()))
    if timestep_indices is None:
        timestep_indices = range(len(full_timeline))

    sat_items = list(propagated_satellites.items())
    for time_index in timestep_indices:
        t = full_timeline[time_index]["time"]
        jd, fr = GetJulianDate(t)

        visible_satellites = []

        for satellite_name, samples in sat_items:
            if time_index >= len(samples):
                continue

            r_teme = samples[time_index]["r"]
            ok, elevation = visibility_check(r_teme, jd, fr, lat, lon)
            if not ok:
                continue

            visible_satellites.append({
                "name": satellite_name,
                "position_km": r_teme,
                "elevation_degrees": elevation
            })

        visibility_at_time.append((t, visible_satellites))
    return visibility_at_time


def checkForCoverage(lat, lon, propagatedSatellites, simulation_duration, beamwidth=15.0, time_step_index=None):
    capacity_sum = 0.0
    capacity_count = 0
    coverage_windows = []
    in_coverage = False
    window_start_time = None

    visibility_by_time = (precompute_data(propagatedSatellites, lat, lon, timestep_indices=[time_step_index])
        if time_step_index is not None else precompute_data(propagatedSatellites, lat, lon))

    for t, visible_satellites in visibility_by_time:
        jd, fr = GetJulianDate(t)
        capacity_this_step = 0.0

        if visible_satellites:
            filtered, optimal = BeamFilter(visible_satellites, jd, fr, lat, lon, obs_alt=0.0, beamwidth_deg=beamwidth)
        else:
            filtered = False

        if filtered:
            link = compute_link_budget(optimal, filtered, jd, fr, lat, lon)
            capacity_this_step = link["capacity_mbps"]

            if not in_coverage:
                in_coverage = True
                window_start_time = t
        else:
            if in_coverage:
                in_coverage = False
                coverage_windows.append((window_start_time, t))

        capacity_sum += capacity_this_step
        capacity_count += 1

    if in_coverage and window_start_time is not None:
        coverage_windows.append(
            (window_start_time, visibility_by_time[-1][0])
        )

    total_seconds = sum((end - start).total_seconds() for start, end in coverage_windows)
    coverage_percent = (total_seconds /(simulation_duration * 3600.0)) * 100.0
    average_capacity = (capacity_sum / capacity_count if capacity_count > 0 else 0.0)

    return {
        "coverage_percent": coverage_percent,
        "coverage_capacity": average_capacity,
    }