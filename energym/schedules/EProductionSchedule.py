import datetime
import pandas as pd
from scipy.signal import savgol_filter
from copy import deepcopy
from datetime import timedelta
from scipy.stats import truncnorm
import numpy as np

from energym.schedules.AbstractSchedule import ScheduleAbstract


# CO2 emissions: g/kWh
CO2dic = {
    "biomass": 230.0,
    "coal": 820.0,
    "gas": 490.0,
    "geothermal": 38.0,
    "hydro": 24.0,
    "nuclear": 12.0,
    "oil": 650.0,
    "solar": 45.0,
    "wind": 11.0,
    "unknown": 700.0,
    "imported": 50.0,
}


class EProductionSchedule(ScheduleAbstract):

    """ Electricity CO2 schedule for CO2 content of electric production"""

    def __init__(self, yearly_profile: pd.DataFrame):

        """yearly profile: profile at 15 minutes samples"""

        self.schedule = deepcopy(yearly_profile)
        self.prediction = deepcopy(yearly_profile)

    def generate_profile(self, start: datetime.datetime, basefreq: int, seed: int):

        # fix numpy seed
        np.random.seed(seed)

        # nb points per day
        nbpoints = 60 // basefreq * 24
        data = deepcopy(self.schedule)

        # Extract percentage and compute CO2 emissions
        lines_prod = np.where(data["imported"].values < 0)[0]
        lines_cons = np.where(data["imported"].values >= 0)[0]
        for key in CO2dic:
            data[key].iloc[lines_prod] = (
                data[key].iloc[lines_prod]
                / (data["production_total"] - data["hydro_storage"]).iloc[lines_prod]
            )
            data[key].iloc[lines_cons] = (
                data[key].iloc[lines_cons]
                / (data["consumption"] - data["hydro_storage"]).iloc[lines_cons]
            )

        data.loc[data["imported"] < 0, "imported"] = 0.0

        data.drop(
            columns=["hydro_storage", "production_total", "consumption"], inplace=True
        )
        dataCO2 = deepcopy(data)

        # Compute CO2 amount
        for key in CO2dic:
            dataCO2[key] = dataCO2[key] * CO2dic[key]

        dataCO2["total"] = dataCO2.sum(axis=1)
        dataCO2.drop(columns=[key for key in CO2dic], inplace=True)

        self.schedule = deepcopy(dataCO2)

        # Interpolate
        range_year = pd.date_range(
            start,
            start + datetime.timedelta(days=365),
            freq="{}min".format(basefreq),
        )[:-1]

        self.schedule = self.schedule.set_index(pd.to_datetime(self.schedule.index))
        if basefreq < 15:
            self.schedule = (
                self.schedule.resample("{}min".format(basefreq)).bfill().dropna()
            )
        else:
            self.schedule = (
                self.schedule.resample("{}min".format(basefreq)).mean().dropna()
            )

        # If there is a length mismatch, replicate the last line
        misma = len(range_year) - len(self.schedule)
        if misma > 0:
            self.schedule = pd.concat(
                [self.schedule, self.schedule[-misma:]], ignore_index=True
            )

        self.schedule.index = range_year
        self.prediction = deepcopy(self.schedule)

        # Randomize the predictor
        for i, (_, df_day) in enumerate(
            self.schedule.groupby(self.schedule.index.date)
        ):
            np.random.seed(seed * i)
            # Get quantiles for week random adjustements
            oldmin, oldmax = (
                df_day["total"].min(),
                df_day["total"].max(),
            )

            delta = oldmax - oldmin
            random_max_fac = 0.3 * np.random.sample() + 0.85
            random_min_fac = 0.3 * np.random.sample() + 0.85

            # Rescale every day prediction randomly to fit between min and max
            df_day["total"] = (
                df_day["total"]
                * (random_max_fac * oldmax - random_min_fac * oldmin)
                / delta
                + oldmax * random_min_fac * oldmin / delta
                - oldmin * random_max_fac * oldmax / delta
            )

            self.schedule.update(df_day)

        self.schedule = pd.Series(
            savgol_filter(
                self.schedule["total"], window_length=5, polyorder=2, mode="nearest"
            ),
            range_year,
        )

        self.prediction = pd.Series(
            savgol_filter(
                self.prediction["total"], window_length=61, polyorder=2, mode="nearest"
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
        return val / 3.6  # Conversion to g/MJ for E+

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
        return val / 3.6  # Conversion to g/MJ for E+
