import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU
from energym.schedules.CPUSchedule import CPUSchedule


INPUTS_SPECS = {
    "Z01_T_HVAC_sp": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 26,
        "default": 19,
    },
    "Z02_T_HVAC_sp": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 26,
        "default": 19,
    },
    "Z02_Fl_Fan_sp": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 7,
        "default": 4,
    },
    "Z01_Fl_Fan_sp": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 7,
        "default": 4,
    },
    "Z01_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z02_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
}

OUTPUTS_SPECS = {
    "Bd_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 18e4,
    },
    "Ext_Irr": {"type": "scalar", "lower_bound": 0, "upper_bound": 1000},
    "Ext_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Ext_T": {"type": "scalar", "lower_bound": -25, "upper_bound": 45},
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 21e4,
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e4,
    },
    "Z01_Fl_Fan": {"type": "scalar", "lower_bound": 0, "upper_bound": 7},
    "Z01_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 7,
    },
    "Z01_EEn_CCDX": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 6e6,
    },
    "Z01_EEn_DEC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e6,
    },
    "Z01_EEn_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e6,
    },
    "Z01_EEn_IEC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e6,
    },
    "Z01_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z01_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z01_T_HVAC_sp_out": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 26,
    },
    "Z01_T_MixAir": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 30,
    },
    "Z01_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z02_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z02_Fl_Fan": {"type": "scalar", "lower_bound": 0, "upper_bound": 7},
    "Z02_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 7,
    },
    "Z02_EEn_CCDX": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 6e6,
    },
    "Z02_EEn_DEC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e6,
    },
    "Z02_EEn_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e6,
    },
    "Z02_EEn_IEC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e6,
    },
    "Z02_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z02_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z02_T_HVAC_sp_out": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 26,
    },
    "Z02_T_MixAir": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 30,
    },
    "Bd_Load_CPU": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
}

default_kpi_options = {
    "kpi1": {"name": "Fa_Pw_All", "type": "avg"},
    "kpi2": {"name": "Z01_T", "type": "avg_dev", "target": [17, 26]},
    "kpi3": {"name": "Z02_T", "type": "avg_dev", "target": [17, 26]},
    "kpi4": {"name": "Z01_T", "type": "tot_viol", "target": [17, 26]},
    "kpi5": {"name": "Z02_T", "type": "tot_viol", "target": [17, 26]},
}


class DataCenter(EnvEPlusFMU):
    """Containing information for the models DatacenterThermostat-v0 and DatacenterTempFan-v0.

    Subclasses EnvEPlusFMU and inherits its behavior. Simulation based details are
    specified in this class and passed to the constructor of EnvEPlusFMU.

    Attributes
    -----------
    cpu_schedule : CPUSchedule
        CPUSchedule object for scheduling and predicting CPU load.

    Methods
    --------
    step(inputs):
        Advances the simulation one timestep.
    predict_cpu(steps):
        Provides a forecast for the CPU schedule.
    """

    def __init__(
        self,
        model_path,
        cpu_schedule,
        start_day=1,
        start_month=1,
        year=2019,
        simulation_days=10,
        weather="USA_NY_NewYork_KennedyAP1",
        kpi_options=None,
    ):
        """
        Parameters
        ----------
        model_path : str
            Specifies the path to the FMU.
        cpu_schedule : CPUSchedule
            CPUSchedule object for scheduling and predicting CPU load.
        start_day : int, optional
            Day of the month to start the simulation, by default 1.
        start_month : int, optional
            Month of the year to start the simulation, by default 1.
        year : int, optional
            Year to start the simulation, by default 2019.
        simulation_days : int, optional
            Number of days the simulation can run for, by default 10.
        weather : str, optional
            Specific weather file to run the simulation, by default
            "USA_NY_NewYork_KennedyAP1".
        kpi_options : dict, optional
            Dict to specify the tracked KPIs, by default None.
        """

        n_steps = 4
        step_size = 15 * 60
        start_date = datetime.date(year, start_month, start_day)
        delta = start_date - datetime.date(year, 1, 1)
        start_time = delta.total_seconds()
        stop_time = (
            start_time + n_steps * 24 * simulation_days * step_size
        )
        if kpi_options is None:
            kpi_options = default_kpi_options

        self.cpu_schedule = cpu_schedule

        super().__init__(
            model_path,
            start_time,
            stop_time,
            step_size,
            weather,
            INPUTS_SPECS,
            OUTPUTS_SPECS,
            kpi_options,
        )

    def step(self, inputs):
        """Advances the simulation one timestep.

        Calls the step() method of EnvFMU.

        Parameters
        ----------
        inputs : dict
            Inputs for the system. Keys are input names, values are iterables of input values.
            If not defined, assumes no inputs required.

        Returns
        -------
        out : dict
            Outputs for the system.
        """
        minute, hour, day, month = self.get_date()
        date = datetime.datetime(2019, month, day, hour, minute)
        cpu_val = self.cpu_schedule.get(date)
        inputs["Bd_Load_CPU_sp"] = [cpu_val]
        out = super().step(inputs=inputs)
        return out

    def __predict_cpu(self, steps):
        """Provides a forecast for the CPU schedule.

        Parameters
        ----------
        steps : int
            Number of forecast steps.

        Returns
        -------
        predictions : list
            List of predicted values.
        """
        minute, hour, day, month = self.get_date()
        date = datetime.datetime(2019, month, day, hour, minute)
        predictions = []
        for _ in range(steps):
            predictions.append(self.cpu_schedule.predict(date))
            date = date + datetime.timedelta(minutes=15)
        return {"Bd_Load_CPU": predictions}

    def get_forecast(self, forecast_length=24, **kwargs):
        forecasts = super().get_forecast(forecast_length, **kwargs)
        predictions = self.__predict_cpu(steps=forecast_length)
        forecasts = {**forecasts, **predictions}
        return forecasts
