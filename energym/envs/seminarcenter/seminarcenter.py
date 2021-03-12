import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU
from energym.schedules.EProductionSchedule import EProductionSchedule


INPUTS_SPECS = {
    "Bd_onoff_HP1_sp": {"type": "discrete", "size": 2, "default": 1},
    "Bd_onoff_HP2_sp": {"type": "discrete", "size": 2, "default": 1},
    "Bd_onoff_HP3_sp": {"type": "discrete", "size": 2, "default": 1},
    "Bd_onoff_HP4_sp": {"type": "discrete", "size": 2, "default": 1},
    "Bd_T_HP1_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
    },
    "Bd_T_HP2_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
    },
    "Bd_T_HP3_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
    },
    "Bd_T_HP4_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
    },
    "Bd_T_AHU_coil_sp": {
        "type": "scalar",
        "lower_bound": 15,
        "upper_bound": 40,
        "default": 30,
    },
    "Bd_T_buffer_sp": {
        "type": "scalar",
        "lower_bound": 15,
        "upper_bound": 70,
        "default": 40,
    },
    "Bd_T_mixer_sp": {
        "type": "scalar",
        "lower_bound": 20,
        "upper_bound": 60,
        "default": 40,
    },
    "Bd_T_Boiler_sp": {
        "type": "scalar",
        "lower_bound": 20,
        "upper_bound": 80,
        "default": 40,
    },
    "Bd_T_HVAC_sp": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 26,
        "default": 20,
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
    "Z03_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z04_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z05_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z06_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z08_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z09_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z10_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z11_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z13_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z14_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z15_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z18_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z19_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z20_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z21_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Z22_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
}


OUTPUTS_SPECS = {
    "Bd_T_Boiler_sp_out": {
        "type": "scalar",
        "lower_bound": 20,
        "upper_bound": 80,
    },
    "Bd_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
    },
    "Bd_Pw_prod": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
    },
    "Bd_Pw_boiler": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e5,
    },
    "Ext_Irr": {"type": "scalar", "lower_bound": 0, "upper_bound": 1000},
    "Ext_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Ext_T": {"type": "scalar", "lower_bound": -15, "upper_bound": 40},
    "Ext_P": {
        "type": "scalar",
        "lower_bound": 80000,
        "upper_bound": 130000,
    },
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
    },
    "Fa_Pw_Pur": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
    },
    "Z01_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z01_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z01_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z02_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z02_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z02_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z03_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z03_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z03_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z04_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z04_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z04_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z05_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z05_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z05_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z06_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z06_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z06_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z08_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z08_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z08_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z09_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z09_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z09_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z10_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z10_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z10_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z11_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z11_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z11_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z13_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z13_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z13_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z14_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z14_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z14_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z15_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z15_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z15_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z18_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z18_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z18_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z19_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z19_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z19_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z20_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z20_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z20_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z21_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z21_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z21_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Z22_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z22_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z22_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Bd_CO2": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 10,
    },
    "Grid_CO2": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e3,
    },
}

default_kpi_options = {
    "kpi1": {"name": "Bd_CO2", "type": "avg"},
    "kpi2": {"name": "Z01_T", "type": "avg_dev", "target": [21, 24]},
    "kpi3": {"name": "Z02_T", "type": "avg_dev", "target": [21, 24]},
    "kpi4": {"name": "Z03_T", "type": "avg_dev", "target": [21, 24]},
    "kpi5": {"name": "Z04_T", "type": "avg_dev", "target": [21, 24]},
    "kpi6": {"name": "Z05_T", "type": "avg_dev", "target": [21, 24]},
    "kpi7": {"name": "Z06_T", "type": "avg_dev", "target": [21, 24]},
    "kpi9": {"name": "Z08_T", "type": "avg_dev", "target": [21, 24]},
    "kpi10": {"name": "Z09_T", "type": "avg_dev", "target": [21, 24]},
    "kpi11": {"name": "Z10_T", "type": "avg_dev", "target": [21, 24]},
    "kpi12": {"name": "Z11_T", "type": "avg_dev", "target": [21, 24]},
    "kpi14": {"name": "Z13_T", "type": "avg_dev", "target": [21, 24]},
    "kpi15": {"name": "Z14_T", "type": "avg_dev", "target": [21, 24]},
    "kpi16": {"name": "Z15_T", "type": "avg_dev", "target": [21, 24]},
    "kpi19": {"name": "Z18_T", "type": "avg_dev", "target": [21, 24]},
    "kpi20": {"name": "Z19_T", "type": "avg_dev", "target": [21, 24]},
    "kpi21": {"name": "Z20_T", "type": "avg_dev", "target": [21, 24]},
    "kpi22": {"name": "Z21_T", "type": "avg_dev", "target": [21, 24]},
    "kpi23": {"name": "Z22_T", "type": "avg_dev", "target": [21, 24]},
    "kpi25": {"name": "Z01_T", "type": "tot_viol", "target": [21, 24]},
    "kpi26": {"name": "Z02_T", "type": "tot_viol", "target": [21, 24]},
    "kpi27": {"name": "Z03_T", "type": "tot_viol", "target": [21, 24]},
    "kpi28": {"name": "Z04_T", "type": "tot_viol", "target": [21, 24]},
    "kpi29": {"name": "Z05_T", "type": "tot_viol", "target": [21, 24]},
    "kpi30": {"name": "Z06_T", "type": "tot_viol", "target": [21, 24]},
    "kpi32": {"name": "Z08_T", "type": "tot_viol", "target": [21, 24]},
    "kpi33": {"name": "Z09_T", "type": "tot_viol", "target": [21, 24]},
    "kpi34": {"name": "Z10_T", "type": "tot_viol", "target": [21, 24]},
    "kpi35": {"name": "Z11_T", "type": "tot_viol", "target": [21, 24]},
    "kpi37": {"name": "Z13_T", "type": "tot_viol", "target": [21, 24]},
    "kpi38": {"name": "Z14_T", "type": "tot_viol", "target": [21, 24]},
    "kpi39": {"name": "Z15_T", "type": "tot_viol", "target": [21, 24]},
    "kpi42": {"name": "Z18_T", "type": "tot_viol", "target": [21, 24]},
    "kpi43": {"name": "Z19_T", "type": "tot_viol", "target": [21, 24]},
    "kpi44": {"name": "Z20_T", "type": "tot_viol", "target": [21, 24]},
    "kpi45": {"name": "Z21_T", "type": "tot_viol", "target": [21, 24]},
    "kpi46": {"name": "Z22_T", "type": "tot_viol", "target": [21, 24]},
}


class Seminarcenter(EnvEPlusFMU):
    """Containing information for the models SeminarcenterThermostat-v0 and SeminarcenterFull-v0.

    Subclasses EnvEPlusFMU and inherits its behavior. Simulation based details are
    specified in this class and passed to the constructor of EnvEPlusFMU.

    Attributes
    -----------
    CO2_schedule : EProductionSchedule
        Schedule specifying the CO2 emission of the current energy mix.

    Methods
    --------
    step(inputs):
        Advances the simulation one timestep.
    predict_co2(steps):
        Provides a forecast for the CO2 schedule.
    """

    def __init__(
        self,
        model_path,
        CO2_schedule,
        start_day=1,
        start_month=1,
        year=2019,
        simulation_days=10,
        weather="DNK_MJ_Horsens1",
        kpi_options=None,
    ):
        """
        Parameters
        ----------
        model_path : str
            Specifies the path to the FMU
        CO2_schedule : EProductionSchedule
            Schedule specifying the CO2 emission of the current energy mix.
        start_day : int, optional
            Day of the month to start the simulation, by default 1
        start_month : int, optional
            Month of the year to start the simulation, by default 1
        year : int, optional
            Year to start the simulation, by default 2019
        simulation_days : int, optional
            Number of days the simulation can run for, by default 10
        weather : str, optional
            Specific weather file to run the simulation, by default
            "DNK_MJ_Horsens1"
        kpi_options : dict, optional
            Dict to specify the tracked KPIs, by default None.
        """

        n_steps = 6
        step_size = 10 * 60
        start_date = datetime.date(year, start_month, start_day)
        delta = start_date - datetime.date(year, 1, 1)
        start_time = delta.total_seconds()
        stop_time = (
            start_time + n_steps * 24 * simulation_days * step_size
        )
        if kpi_options is None:
            kpi_options = default_kpi_options

        self.CO2_schedule = CO2_schedule

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
        CO2_val = self.CO2_schedule.get(date)
        inputs["Grid_CO2_sp"] = [CO2_val]
        out = super().step(inputs=inputs)
        return out

    def __predict_co2(self, steps):
        """Provides a forecast for the CO2 schedule.

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
            predictions.append(self.CO2_schedule.predict(date))
            date = date + datetime.timedelta(minutes=10)
        return {"Grid_CO2": predictions}

    def get_forecast(self, forecast_length=24, **kwargs):
        forecasts = super().get_forecast(forecast_length, **kwargs)
        predictions = self.__predict_co2(steps=forecast_length)
        forecasts = {**forecasts, **predictions}
        return forecasts
