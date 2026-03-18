class CoverageStatsCalculator:

    def __init__(self, duration_hours):
        self.total_coverage = 0.0
        self.count_windows = 0
        self.duration_hours = duration_hours

    def traverse_coverage_windows(self, coverage_windows):
        for (start, end) in coverage_windows:
            duration = (end - start).total_seconds()
            self.total_coverage += duration
            self.count_windows += 1

    def get_average_coverage(self):
        if self.count_windows > 0:
            return (self.total_coverage / self.count_windows) / 60
        else:
            # previous code was potentially dividing this by 60
            return 0.0

    def get_coverage_percent(self):
        return (self.total_coverage / (self.duration_hours * 3600.0)) * 100.0

    def get_total_coverage(self):
        return self.total_coverage / 60


