from datetime import datetime, timezone

class LinkBudgetConfig:
    TRANSMIT_POWER_DB = 46
    RECEIVER_GAIN_DBI = 33
    FREQUENCY_HZ = 12e9
    OTHER_LOSSES_DB = 0.0


class SimulationConfig:
    LAT_MIN = 51.3
    LAT_MAX = 56.0
    LON_MIN = -10.7
    LON_MAX = -5.5
    LAT_LON_STEP = 0.5

    PROPAGATION_TIME_STEP = 60
    SIMULATION_DURATION_HOURS = 2

    SIMULATION_START = datetime(year=2026, month=5, day=19, hour=12, minute=0, second=0, tzinfo=timezone.utc)

    BEAMWIDTH = 15.0


class ContentionConfig:
    USE_CONTENTION = False
    NUM_USERS = 20
    METHOD = "equal"


class TLEoption:
    OPTIONS = [
        "Starlink (DTC Only)",
        "Starlink (All)",
        "OneWeb",
        "Kuiper"
    ]

    tle_choice = "OneWeb"