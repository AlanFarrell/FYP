import math
from dataclasses import dataclass


@dataclass
class LinkBudgetResults:
    signal_db: float
    interference_db: float
    noise_db: float

    snr_db: float
    sir_db: float
    sinr_db: float

    capacity_mbps: float


class LinkBudgetCalculations:

    def __init__(self,
                 signal_power_watts=None,
                 interference_power_watts=None,
                 noise_figure_db=1.0,
                 bandwidth_hz=20e6):

        self.signal_power_watts = signal_power_watts or 0.0
        self.interference_power_watts = interference_power_watts or 0.0
        self.noise_figure_db = noise_figure_db
        self.bandwidth_hz = bandwidth_hz

    @staticmethod
    def watts_to_db(watts: float) -> float:
        return 10 * math.log10(watts) if watts > 0 else float('-inf')

    def noise_power(self) -> float:
        k = 1.380649e-23
        T = 290.0
        nf_linear = 10 ** (self.noise_figure_db / 10)
        return k * T * self.bandwidth_hz * nf_linear

    def compute(self) -> LinkBudgetResults:

        noise_watts = self.noise_power()

        # SNR
        snr_watts = (
            self.signal_power_watts / noise_watts
            if noise_watts > 0 else float('inf')
        )

        # SIR
        if self.interference_power_watts > 0:
            sir_watts = self.signal_power_watts / self.interference_power_watts
        else:
            sir_watts = float('inf')

        # SINR
        sinr_watts = self.signal_power_watts / (
            self.interference_power_watts + noise_watts
        )

        # Shannon capacity
        capacity_bps = self.bandwidth_hz * math.log2(1 + sinr_watts)
        capacity_mbps = capacity_bps / 1e6

        return LinkBudgetResults(
            signal_db=self.watts_to_db(self.signal_power_watts),
            interference_db=self.watts_to_db(self.interference_power_watts),
            noise_db=self.watts_to_db(noise_watts),

            snr_db=self.watts_to_db(snr_watts),
            sir_db=self.watts_to_db(sir_watts),
            sinr_db=self.watts_to_db(sinr_watts),

            capacity_mbps=capacity_mbps
        )