from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from sgp4.api import Satrec
from datetime import timedelta
from config import SimulationConfig

from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef

def quickPropagate(TLEs):

    satellites = [
        (name.strip(), Satrec.twoline2rv(line1.strip(), line2.strip()))
        for name, line1, line2 in TLEs
    ]

    end_time = SimulationConfig.SIMULATION_START + timedelta(hours=SimulationConfig.SIMULATION_DURATION_HOURS)
    step_td = timedelta(seconds=SimulationConfig.PROPAGATION_TIME_STEP)
    propagated = {name: [] for name, _ in satellites}

    current_time = SimulationConfig.SIMULATION_START
    while current_time < end_time:
        jd, fr = GetJulianDate(current_time)
        timestamp = current_time.timestamp()

        for name, sat in satellites:
            e, r, v = sat.sgp4(jd, fr)
            if e == 0:
                satellite_x, satellite_y, satellite_z, = teme_to_ecef(r, jd, fr)
                propagated[name].append((timestamp, satellite_x, satellite_y, satellite_z))

        current_time += step_td

    return propagated