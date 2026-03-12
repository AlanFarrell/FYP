import math
from dataclasses import dataclass
import numpy as np
from math import log10


def linkbudget(
        signal_power_w= None,
        interferance_power = None,
        noise_figure_db = 1.0,
        bandwidth = 20e6):

    def to_db(x):
        return 10 * math.log10(x) if x > 0 else -999.0

    #noise power
    k = 1.380649e-23
    T = 290.0
    nf_lin = 10 ** (noise_figure_db / 10)
    noise_power = k * T * bandwidth * nf_lin


    #default values in case of missing values
    if signal_power_w is None:
        signal_power_w = 0.0
    if interferance_power is None:
        interferance_power = 0.0




    #SNR, SIR, SINR
    snr_lin = signal_power_w / noise_power if noise_power > 0 else float("inf")
    snr_db = to_db(snr_lin)

    if interferance_power > 0:
        sir_lin = signal_power_w /interferance_power
        sir_db = to_db(sir_lin)
    else:
        sir_lin = float("inf")
        sir_db = float("inf")

    sinr_lin = signal_power_w / (interferance_power + noise_power)
    sinr_db = to_db(sinr_lin)

    #shannon capacity
    capacity_bps = bandwidth * math.log10(1+ sinr_lin)
    capacity_mbps = capacity_bps / 1e6


    signal_db = to_db(signal_power_w)
    interference_db = to_db(interferance_power)
    noise_db = to_db(noise_figure_db)

    return{
        "signal_dbw": signal_db,
        "interference_dbw": interference_db,
        "noise_dbw": noise_db,

        "snr_dbw": snr_db,
        "sir_dbw": sir_db,
        "sinr_dbw": sinr_db,

        "capacity_mbps": capacity_mbps,
    }


