import pandas as pd
import datetime
import random
import numpy as np
from copy import deepcopy

from random import normalvariate, randint
from scipy.stats import truncnorm


from energym.schedules.AbstractSchedule import ScheduleAbstract


class ElectricVehicleSchedule(ScheduleAbstract):

    """Base class for electric vehicle schedules. Consumption schedules are in
    percentage of battery capacity"""

    def __init__(
        self,
        daily_weekdays_rate: float,  # total daily consumption during weekdays % of Capacity
        daily_weekends_rate: float,  # total daily consumption driven during weekends % of Capacity
        discharge_rate: float,  # discharge power/Capacity
    ):

        self.daily_weekdays_rate = daily_weekdays_rate
        self.daily_weekends_rate = daily_weekends_rate
        self.discharge_rate = discharge_rate

        self.schedule = None
        self.prediction = None

    def generate_profile(self, start: datetime.datetime, basefreq: int, seed: int):

        """Generate discharge EV profile around mean. Discharge rate not meant to be realistic,
        but used to generate correct consumption profiles"""

        # Initial time range
        range_year = pd.date_range(
            start,
            start + datetime.timedelta(days=365),
            freq="{}min".format(basefreq),
        )[:-1]

        # Create clock
        clock_template = [
            datetime.datetime(1, 1, 1) + x * datetime.timedelta(minutes=basefreq)
            for x in range(0, 60 * 24 // basefreq)
        ]
        clock_template = pd.Series([elt.time() for elt in clock_template])

        # Create, weeks, days hours and minutes columns
        self.schedule = pd.DataFrame(
            {
                "Time": range_year,
                "Discharge_rate": 0,
                "Available": 0,
            }
        )
        self.schedule["Week"] = self.schedule["Time"].dt.week
        self.schedule["Day"] = self.schedule["Time"].dt.weekday
        self.schedule["Hour"] = self.schedule["Time"].dt.hour
        self.schedule["Minute"] = self.schedule["Time"].dt.minute
        self.prediction = deepcopy(self.schedule)

        # Truncated normal distributions for weekdays and weekends
        std_week = 10
        std_weekend = 30
        awday, bwday = (
            self.daily_weekdays_rate * 0.5 - self.daily_weekdays_rate
        ) / std_week, (
            90 - self.daily_weekdays_rate
        ) / std_week  # Max 90% consumption of initial capacity

        aend, bend = (
            self.daily_weekends_rate * 0.1 - self.daily_weekends_rate
        ) / std_weekend, (
            90 - self.daily_weekends_rate
        ) / std_weekend  # Max 90% consumption of initial capacity

        # Replace each day by a random profile, with fix seed, and fix day and time arrival

        for (
            _,
            df_day,
        ) in self.schedule.groupby(self.schedule["Time"].dt.date):

            new_seed = int(df_day["Day"].iloc[0] + 1000 * df_day["Week"].iloc[0] + seed)

            random.seed(new_seed)

            if 0 <= df_day["Day"].iloc[0] <= 4:  # weekdays: low variations

                time_arrival = time_normal_distribution(
                    (17, 30), 30, basefreq, clock_template
                )

                time_departure = time_normal_distribution(
                    (7, 0), 30, basefreq, clock_template
                )

                time_departure_pred = datetime.time(6, 30, 0)

                time_arrival_pred = datetime.time(18, 0, 0)

                consumption = truncnorm.rvs(
                    awday,
                    bwday,
                    loc=self.daily_weekdays_rate,
                    scale=std_week,
                    size=1,
                    random_state=new_seed,
                )

                consumption_pred = (
                    self.daily_weekdays_rate
                )  # fixed value for prediction

            else:  # weekends: large variations

                time_arrival = time_normal_distribution(
                    (17, 30), 3 * 60, basefreq, clock_template
                )

                time_departure = time_normal_distribution(
                    (10, 0), 2 * 60, basefreq, clock_template  # 120 mintes==2hours
                )

                time_departure_pred = datetime.time(8, 0, 0)

                time_arrival_pred = datetime.time(20, 30, 0)

                consumption = truncnorm.rvs(
                    aend,
                    bend,
                    loc=self.daily_weekends_rate,
                    scale=std_weekend,
                    size=1,
                    random_state=new_seed,
                )
                consumption_pred = self.daily_weekends_rate

            df_day_pred = deepcopy(df_day)
            df_day = update_df_day(
                df_day,
                time_arrival,
                time_departure,
                consumption,
                basefreq,
                self.discharge_rate,
            )
            df_day_pred = update_df_day(
                df_day_pred,
                time_arrival_pred,
                time_departure_pred,
                consumption_pred,
                basefreq,
                self.discharge_rate,
            )

            self.schedule.update(df_day)
            self.prediction.update(df_day_pred)

        self.schedule = self.schedule.set_index("Time")
        self.prediction = self.prediction.set_index("Time")

    def get(self, t: datetime.datetime):

        """Get schedule at time t. Year agostic method"""
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

        val = self.schedule.iloc[indices[where]]["Discharge_rate"]
        return val

    def predict(self, t: datetime.datetime):

        """Get prediction at time t. Year agostic method"""
        day = t.day
        month = t.month
        hour = t.hour
        minute = t.minute

        years = list(set(list(self.schedule.index.year)))
        dts = [datetime.datetime(y, month, day, hour, minute) for y in years]
        indices = [self.prediction.index.get_loc(dt, method="nearest") for dt in dts]
        index_values = [
            np.abs((self.prediction.index[indices[i]] - dts[i]).total_seconds())
            for i in range(len(indices))
        ]
        where = np.argmin(index_values)

        val = self.prediction.iloc[indices[where]]["Discharge_rate"]
        return val


####################################  HELPERS FOR MODEL STOCHASTICS ###################


# =============================================================================
# Function returning probable time according to mean and standard deviation given, used for Home users
# =============================================================================
def time_normal_distribution(
    mean, stddev, freq, clock_template
):  # mean = tuple(hour and minute), stddev in minutes
    i_mean = clock_template[clock_template == datetime.time(*mean)].index[0]
    while True:
        index = int(normalvariate(i_mean, stddev / freq) + 0.5)
        if 0 <= index < len(clock_template):
            return clock_template[index]


# =============================================================================
# Function returning probable start and end time according to min and max times (random) and duration, used for Shopping and Fast Charging users
# =============================================================================
def time_random_interval(
    start, end, duration, dur_stddev, freq, clock_template
):  # start, end = tuple(hour and minute), duration/stddev in minutes
    i_start = clock_template[clock_template == datetime.time(*start)].index[0]
    i_end = clock_template[clock_template == datetime.time(*end)].index[0]
    i_arrival = randint(i_start, i_end)
    while True:
        i_duration = int(normalvariate(duration / freq, dur_stddev / freq) + 0.5)
        if 0 <= i_arrival + i_duration < len(clock_template) and i_duration > 0:
            return clock_template[i_arrival], clock_template[i_arrival + i_duration]


# =============================================================================
# Function returning probable start and end time according to probable arrival and duration, used for Work users
# =============================================================================
def time_normal_interval(mean, duration, mean_stddev, dur_stddev, freq, clock_template):
    i_mean = clock_template[clock_template == datetime.time(*mean)].index[0]
    while True:
        index = int(normalvariate(i_mean, mean_stddev / freq) + 0.5)
        i_duration = int(normalvariate(duration / freq, dur_stddev / freq) + 0.5)
        if 0 <= index < len(clock_template) and i_duration > 0:
            return clock_template[index], clock_template[index + i_duration]


def update_df_day(
    df_day,
    time_arrival,
    time_departure,
    consumption,
    basefreq,
    discharge_rate,
):
    time_ar = datetime.timedelta(
        hours=time_arrival.hour,
        minutes=time_arrival.minute,
        seconds=time_arrival.second,
    )
    time_dep = datetime.timedelta(
        hours=time_departure.hour,
        minutes=time_departure.minute,
        seconds=time_departure.second,
    )

    len_usage = max(((time_ar - time_dep).total_seconds()) / (basefreq * 60), 1e-4)

    factor = 60 // basefreq  # nbpoints per hour

    rate = min(consumption * factor / (100.0 * len_usage * discharge_rate), 1.0)

    if type(rate) == list:
        rate = rate[0]

    df_day.loc[df_day["Time"].dt.time >= time_arrival, "Available"] = 1
    df_day.loc[df_day["Time"].dt.time <= time_departure, "Available"] = 1
    df_day.loc[df_day["Available"] == 0, "Discharge_rate"] = (
        df_day.loc[df_day["Available"] == 0, "Discharge_rate"] * 0.0 + rate
    )

    return df_day
