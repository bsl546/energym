import datetime
import pandas as pd
from scipy.signal import savgol_filter
from copy import deepcopy
from datetime import timedelta
from scipy.stats import truncnorm
import numpy as np

from energym.schedules.AbstractSchedule import ScheduleAbstract


class CPUSchedule(ScheduleAbstract):

    """ CPU schedule class: to create a random cpu profile from a weekly CPU schedule profile"""

    def __init__(self, weekly_profile: pd.DataFrame, profile_ts: int):
        """Profile ts: time scale of profile in seconds"""

        # Fix first timedate
        date_start = datetime.datetime(2019, 10, 19)
        weekly_profile["timestamp"] = [
            date_start + timedelta(seconds=p * profile_ts)
            for p in range(len(weekly_profile))
        ]
        weekly_profile = weekly_profile.set_index("timestamp")
        self.schedule = deepcopy(weekly_profile)
        self.prediction = deepcopy(weekly_profile)

    def generate_profile(self, start: datetime.datetime, basefreq: int, seed: int):

        # fix numpy seed
        np.random.seed(seed)

        # Initial time range
        range_year = pd.date_range(
            start,
            start + datetime.timedelta(days=365),
            freq="{}min".format(basefreq),
        )[:-1]

        # nb points per day
        nbpoints = 60 // basefreq * 24

        # Reformat weekly based schedule, copy over a year
        # using a max min rescaling for every day of the week
        self.schedule = self.schedule.resample("{}min".format(basefreq)).mean().dropna()

        # Get quantiles for week random adjustements
        high, low = (
            self.schedule["cpu_util_percent_mean"].quantile(0.95),
            self.schedule["cpu_util_percent_mean"].quantile(0.05),
        )
        oldmin, oldmax = (
            self.schedule["cpu_util_percent_mean"].min(),
            self.schedule["cpu_util_percent_mean"].max(),
        )
        delta = oldmax - oldmin
        amin, bmin = (0.9 * -low) / 5.0, (1.1 * low - low) / 5.0
        amax, bmax = (high * 0.9 - high) / 5.0, (max(1.1 * high, 100) - high) / 5.0
        random_min = truncnorm.rvs(
            amin,
            bmin,
            loc=low,
            scale=5,
            size=52,
            random_state=seed,
        )
        random_max = truncnorm.rvs(
            amax,
            bmax,
            loc=high,
            scale=5,
            size=52,
            random_state=seed,
        )

        # Multiply patterns by mean and max to have varying peaks every week
        all_weeks = pd.concat(
            [
                (
                    self.schedule["cpu_util_percent_mean"]
                    * (random_max[p] - random_min[p])
                    / delta
                    + oldmax * random_min[p] / delta
                    - oldmin * random_max[p] / delta
                )
                for p in range(52)
            ]
            + [self.schedule["cpu_util_percent_mean"][0:nbpoints]]
        )

        all_weeks.index = range_year

        all_weeks_noscale = pd.concat(
            [self.schedule["cpu_util_percent_mean"] for p in range(52)]
            + [self.schedule["cpu_util_percent_mean"][0:nbpoints]]
        )
        all_weeks_noscale.index = range_year
        self.prediction = deepcopy(all_weeks_noscale)

        # Add random noise
        std = pd.concat(
            [self.schedule["cpu_util_percent_var"] for p in range(52)]
            + [self.schedule["cpu_util_percent_var"][0:nbpoints]]
        )
        std.index = range_year
        # randomize std values and clip
        std = np.clip(
            std * np.random.normal(size=len(std)),
            -std.max() / 2.0,
            std.max() / 2.0,
        )
        self.schedule = deepcopy(all_weeks)
        self.schedule = np.clip(
            self.schedule + std,
            0.0,
            100.0,
        )

        self.prediction = pd.Series(
            savgol_filter(
                self.prediction, window_length=51, polyorder=2, mode="nearest"
            ),
            range_year,
        )

    def get(self, t: datetime.datetime):
        """Get schedule at time t"""

        day = t.day
        month = t.month
        hour = t.hour
        minute = t.minute

        years = list(set(list(self.schedule.index.year)))
        dts = [datetime.datetime(y, month, day, hour, minute) for y in years]
        indices = [self.schedule.index.get_loc(dt, method="nearest") for dt in dts]
        index_values = [
            np.abs((self.schedule.index[indices[i]] - dts[i]).total_seconds())
            for i in range(len(indices))
        ]
        where = np.argmin(index_values)

        val = self.schedule.iloc[indices[where]]
        return val / 100.0  # Get val between 0 and 1

    def predict(
        self,
        t: datetime.datetime,
    ):
        """Get prediction at time t"""
        day = t.day
        month = t.month
        hour = t.hour
        minute = t.minute

        years = list(set(list(self.prediction.index.year)))
        dts = [datetime.datetime(y, month, day, hour, minute) for y in years]
        indices = [self.prediction.index.get_loc(dt, method="nearest") for dt in dts]
        index_values = [
            np.abs((self.prediction.index[indices[i]] - dts[i]).total_seconds())
            for i in range(len(indices))
        ]
        where = np.argmin(index_values)

        val = self.prediction.iloc[indices[where]]
        return val / 100.0  # Get val between 0 and 1
