from sgp4.api import jday
from datetime import datetime, timezone

def GetJulianDate(when_utc=None):
    """
    Convert a datetime (UTC) into Julian date values for SGP4: (jd, fr).
    If no time is provided, uses the current UTC time.
    """
    if when_utc is None:
        when_utc = datetime.now(timezone.utc)

    jd, fr = jday(
        when_utc.year,
        when_utc.month,
        when_utc.day,
        when_utc.hour,
        when_utc.minute,
        when_utc.second + when_utc.microsecond / 1e6
    )

    return jd, fr