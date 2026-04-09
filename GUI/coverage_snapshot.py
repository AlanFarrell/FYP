import numpy as np
from orbit.HelperFucntions.GeodeticToECEF import LatLonToECEF
from orbit.HelperFucntions.GetJulianDate import GetJulianDate
from orbit.BeamWidth import BeamFilter
from LinkBudgetCalculations.ComputeLinkBudget import compute_link_budget
from orbit.HelperFucntions.TEMEtoECEF import teme_to_ecef

precomputed_data = {}

def precompute_satellite_data(propagatedSatellites, timestep_index):
    satellite_positions = []
    satellite_names = []

    if timestep_index in precomputed_data:
        return precomputed_data[timestep_index]

    timeline_entry = next(iter(propagatedSatellites.values()))[timestep_index]
    t = timeline_entry["time"]
    jd, fr = GetJulianDate(t)

    for name, samples in propagatedSatellites.items():
        if timestep_index < len(samples):
            r_teme = samples[timestep_index]["r"]
            r_ecef = teme_to_ecef(r_teme, jd, fr)
            satellite_positions.append(r_ecef)
            satellite_names.append(name)

    satellite_positions = np.array(satellite_positions)
    precomputed_data[timestep_index] = (satellite_positions, satellite_names, jd, fr)
    return satellite_positions, satellite_names, jd, fr


def checkCoverageSnapshot(lat, lon, propagatedSatellites, timestep_index, beamwidth=15.0):
    visible_satellites = []
    satellite_positions, satellite_names, jd, fr = precompute_satellite_data(propagatedSatellites, timestep_index)
    observer_ecef = np.array(LatLonToECEF(lat, lon, 0.0))
    timeline_entry = next(iter(propagatedSatellites.values()))[timestep_index]
    t = timeline_entry["time"]

    if len(satellite_positions) == 0:
        return {"coverage_percent": 0, "coverage_capacity": 0}

    los = satellite_positions - observer_ecef
    los_normalised = np.linalg.norm(los, axis=1)
    los_unit = los / los_normalised[:, None]
    up = observer_ecef / np.linalg.norm(observer_ecef)
    dot = np.sum(los_unit * up, axis=1)
    elevation = np.degrees(np.arcsin(dot))

    visibility_mask = elevation > 15

    if not np.any(visibility_mask):
        return {"coverage_percent": 0, "coverage_capacity": 0}


    for i, name in enumerate(np.array(satellite_names)[visibility_mask]):
        visible_satellites.append({
            "name": name,
            "position_km": satellite_positions[visibility_mask][i],
            "elevation_degrees": elevation[visibility_mask][i]
        })

    filtered_satellites, optimal_satellite = BeamFilter(visible_satellites, jd, fr, lat, lon, obs_alt=0.0, beamwidth_deg=beamwidth)

    if not filtered_satellites:
        return {"coverage_percent": 0, "coverage_capacity": 0}

    data_rate = compute_link_budget(optimal_satellite, filtered_satellites, jd, fr, lat, lon)

    return {
        "coverage_percent": 100,
        "coverage_capacity": data_rate["capacity_mbps"]
    }
