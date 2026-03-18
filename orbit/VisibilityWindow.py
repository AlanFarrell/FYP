from datetime import datetime, timedelta, timezone
from typing import Any

from orbit.propagate import satellite_positions


def coverage_time(obs_lat, obs_lon, lines, dtc_only=False, verbose=False):


    duration_hours = 2
    step_frequency = 30
    total_coverage = 0.0
    count_windows = 0

    start = datetime.now(timezone.utc)
    end = start + timedelta(hours=duration_hours)
    dt = timedelta(seconds=step_frequency)

    print(f"Checking satellite coverage from {start} to {end}")


    #for tracking current state of coverage
    in_coverage = False
    window_start = None
    coverage_windows = []

    time = start

    while time <= end:
        filtered_satellites, optimal_satellite = satellite_positions(
            when_utc=time,
            lines=lines,
            obs_lat=obs_lat,
            obs_lon=obs_lon,
            verbose=False
            )

        if dtc_only:
            filtered_satellites = dtc_filter(filtered_satellites)
        coverage_available = len(filtered_satellites) > 0

        if coverage_available and not in_coverage:
            in_coverage = True
            window_start = time

        if not coverage_available and in_coverage:
            in_coverage = False
            coverage_windows.append((window_start, time))

        last_time = time
        time += dt

    if in_coverage and window_start:
        coverage_windows.append((window_start, last_time))

    average_coverage, coverage_percent, total_coverage = compute_coverage_stats(count_windows, coverage_windows,
                                                                                duration_hours, total_coverage)

    return {
        "windows" : coverage_windows,
        "total(mins)" : total_coverage,
        "avg_coverage(mins)" : average_coverage,
        "coverage_percent" : coverage_percent,
    }



def compute_coverage_stats(count_windows: int, coverage_windows: list[Any], duration_hours: int,
                           total_coverage: float) -> tuple[float, float, float]:
    for (start, end) in coverage_windows:
        duration = (end - start).total_seconds()
        total_coverage += duration
        count_windows += 1

    if count_windows > 0:
        avg_coverage = total_coverage / count_windows
    else:
        avg_coverage = 0.0

    coverage_percent = (total_coverage / (duration_hours * 3600.0)) * 100.0
    total_coverage = total_coverage / 60.0
    average_coverage = avg_coverage / 60.0
    return average_coverage, coverage_percent, total_coverage



def dtc_filter(filtered_satellites):
    return [s for s in filtered_satellites if "DTC" in s["name"].upper()]

