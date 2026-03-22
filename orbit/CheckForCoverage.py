from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.isVisible import is_visible
from orbit.BeamWidth import BeamFilter
from LinkBudgetCalculations.linkbudget import LinkBudgetCalculations
from LinkBudgetCalculations.ComputeLinkBudget import compute_link_budget


import numpy as np

def checkForCoverage(lat, lon, propagatedSatellites, simulation_duration, beamwidth=15.0):
    coverage_windows = []
    in_coverage = False
    window_start = None

    timeline = [entry["time"] for entry in next(iter(propagatedSatellites.values()))]

    timestep_capacities = []

    for idx, t in enumerate(timeline):
        jd, fr = GetJulianDate(t)
        visible_satellites = []
        for satellite_name, samples in propagatedSatellites.items():
            sat_data = samples[idx]
            r_teme = sat_data["r"]

            ok, elevation = is_visible(r_teme, jd, fr, lat, lon)
            if not ok:
                continue

            visible_satellites.append({
                "name": satellite_name,
                "position_km": r_teme,
                "elevation_degrees": elevation
            })

        filtered_satellites, optimal_satellite = BeamFilter(
            visible_satellites,
            jd, fr, lat, lon,
            obs_alt=0.0,
            beamwidth_deg=beamwidth
        )

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


    total_secs = sum((end - start).total_seconds() for start, end in coverage_windows)
    coverage_percent = (total_secs / (simulation_duration * 3600)) * 100.0
    total_mins = total_secs / 60.0
    average_capacity = np.mean(timestep_capacities) if timestep_capacities else 0.0

    return {
        "coverage_windows": coverage_windows,
        "total_minutes": total_mins,
        "coverage_percent": coverage_percent,
        "coverage_capacity": average_capacity,
    }

