from typing import Dict
import numpy as np


class Stats:
    def __init__(self) -> None:
        self._vals = []
        self._min = None
        self._max = None
        self._mean = None
        self._median = None
        self._std = None
        self._25 = None
        self._50 = None
        self._75 = None

    @staticmethod
    def to_float(val):
        try:
            return float(val)
        except:
            return None

    def get_stats(self) -> Dict:
        # calculate mean, std and percentiles only when required
        self.calculate_mean()
        self.calculate_std()
        self.calculate_25()
        self.calculate_50()
        self.calculate_75()

        return {
            'min': self._min,
            'max': self._max,
            'mean': self._mean,
            'median': self._median,
            'std': self._std,
            '25': self._25,
            '50': self._50,
            '75': self._75
        }

    def update_min(self, val: float) -> None:
        if self._min is None:
            self._min = val

        if val < self._min:
            self._min = val

    def update_max(self, val: float) -> None:
        if self._max is None:
            self._max = val

        if val > self._max:
            self._max = val

    def calculate_mean(self) -> None:
        self._mean = sum(self._vals) / len(self._vals)

    def calculate_std(self) -> None:
        self._std = np.std(self._vals)

    def calculate_25(self) -> None:
        self._25 = np.percentile(self._vals, 25)

    def calculate_50(self) -> None:
        self._50 = np.percentile(self._vals, 50)

    def calculate_75(self) -> None:
        self._75 = np.percentile(self._vals, 75)

    def update_stats(self, val) -> None:
        val = self.to_float(val)
        if val is None:
            return

        self._vals.append(val)
        self.update_min(val=val)
        self.update_max(val=val)
