from datetime import datetime, timedelta, timezone
from orbit.propagate import satellite_positions


def coverage_time(obs_lat, obs_lon, lines, dtc_only=False, verbose=False):


    duration_hours = 24
    step_frequency = 10

    start = datetime.now(timezone.utc)
    end = start + timedelta(hours=duration_hours)
    dt = timedelta(seconds=step_frequency)

    print(f"Checking satellite coverage from {start} to {end}")


    #for tracking current state of coverage
    in_coverage = False
    window_start = None
    coverage_windows = []
    last_time = start



    time = start

    while time <= end:
        filtered, best = satellite_positions(
            when_utc=time,
            lines=lines,
            obs_lat=obs_lat,
            obs_lon=obs_lon,
            verbose=False
            )



        if dtc_only:
            filtered = [s for s in filtered if "DTC" in s["name"].upper()]
        if verbose:
            if dtc_only:
                print("[summary] Satellites with viable Beamwidth (DTC only):")
            else:
                print("[summary] Satellites with viable Beamwidth (at a time instant):")
            if filtered:
                for s in sorted(filtered, key=lambda x: x["name"]):
                    print(f"  - {s['name']}")
            else:
                print("  (none)")
            print(f"Time: {time.strftime('%H:%M:%S')} | lat lon: {obs_lat:.4f}, {obs_lon:.4f}")
            print()

        coverage_available = len(filtered) > 0

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

    total_coverage = 0.0
    count_windows = 0

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


    return {
        "windows" : coverage_windows,
        "total(mins)" : total_coverage,
        "avg_coverage(mins)" : average_coverage,
        "coverage_percent" : coverage_percent,
    }