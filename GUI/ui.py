import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import numpy as np
from datetime import timedelta

from GUI.coverage_snapshot import checkCoverageSnapshot
from orbit.HelperFucntions.PullTLEs import get_starlink_tles
from orbit.QuickPropagate import quickPropagate
from orbit.coverage_calculations import simulation_parameters, generate_grid
from GUI.SnapShotHeatmap import generate_cartopy_heatmap


@st.cache_data
def load_tles(dtc_only):
    return get_starlink_tles(dtc_only=dtc_only)

@st.cache_data
def propagate_full_day(tle_data):
    return quickPropagate(tle_data, duration=24, step=300)

st.title("Starlink Coverage Demo – Ireland")
st.write("Use the slider below to visualize how Starlink coverage changes throughout the day.")

sim_params = simulation_parameters()
lats, lons, _ = generate_grid(sim_params)
dtc_only = st.checkbox("Filter to DTC-only satellites", value=False)
tle_data = load_tles(dtc_only)
propagated = propagate_full_day(tle_data)
coverage_grid = np.zeros((len(lats), len(lons)))
capacity_grid = np.zeros((len(lats), len(lons)))
first_sat = next(iter(propagated.values()))
timeline = [entry["time"] for entry in first_sat]

selected_dt = st.slider(
        "Select time (UTC)",
        min_value=timeline[0],
        max_value=timeline[-1],
        value=timeline[len(timeline) // 2],
        step=timedelta(minutes=5),
        format="DD/MM/YY - hh:mm",
    )

timestep = min(range(len(timeline)), key=lambda i: abs(timeline[i] - selected_dt))

if st.button("Start Demo"):
    st.info("Loading TLEs and propagating 24 hours... please wait a moment.")
    st.success("Propagation complete! Use the slider below.")
    st.write("### Selected Time:", selected_dt.strftime('%H:%M:%S UTC'))
    st.info("Computing coverage at selected time...")

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            stats = checkCoverageSnapshot(lat, lon, propagated, timestep)
            coverage_grid[i, j] = stats["coverage_percent"]
            capacity_grid[i, j] = stats["coverage_capacity"]

    figure1 = generate_cartopy_heatmap(sim_params, coverage_grid, title=f"Coverage Percentage at {selected_dt.strftime('%H:%M:%S UTC')}", colourBarLabel="Coverage (%)")
    figure2 = generate_cartopy_heatmap(sim_params, capacity_grid, title=f"Capacity at {selected_dt.strftime('%H:%M:%S UTC')}", colourBarLabel="Capacity (Mbps)")

    st.pyplot(figure1)
    st.pyplot(figure2)