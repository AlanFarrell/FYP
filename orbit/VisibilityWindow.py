from datetime import datetime, timedelta, timezone
from orbit.propagate import satellite_positions


def coverage_time(obs_lat, obs_lon, lines):


    duration_hours = 1
    step_frequency = 60 #recheck satellite propagation every x seconds
    total_coverage = 0
    count_windows = 0
    average_coverage = 0

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

    for(start, end) in coverage_windows:
        duration = (end - start).total_seconds()
        total_coverage += duration
        count_windows += 1

    if count_windows > 0:
        avg_coverage = total_coverage / count_windows

        coverage_percent = (total_coverage / (duration_hours*3600)) * 100
        total_coverage = total_coverage/60
        average_coverage = avg_coverage/60

    return {
        "windows" : coverage_windows,
        "total(mins)" : total_coverage,
        "avg_coverage(mins)" : average_coverage,
        "coverage_percent" : coverage_percent,
    }