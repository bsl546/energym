import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU

INPUTS_SPECS = {
    "P1_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "P2_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "P3_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "P4_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
    },
    "Bd_T_HP_sp": {
        "type": "scalar",
        "lower_bound": 35,
        "upper_bound": 55,
        "default": 45,
    },
    "P1_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
    },
    "P2_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
    },
    "P3_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
    },
    "P4_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
    },
    "HVAC_onoff_HP_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
    },
    "Bd_Pw_Bat_sp": {
        "type": "scalar",
        "lower_bound": -1,
        "upper_bound": 1,
        "default": 0,
    },
    "Bd_Ch_EVBat_sp": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "default": 0,
    },
}


OUTPUTS_SPECS = {
    "Ext_T": {"type": "scalar", "lower_bound": -10, "upper_bound": 40},
    "Ext_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Ext_Irr": {"type": "scalar", "lower_bound": 0, "upper_bound": 1000},
    "Ext_P": {
        "type": "scalar",
        "lower_bound": 80000,
        "upper_bound": 130000,
    },
    "P3_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "P4_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "P2_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "P1_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
    },
    "Bd_T_HP_sp_out": {
        "type": "scalar",
        "lower_bound": 35,
        "upper_bound": 55,
    },
    "P1_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "P2_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "P3_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "P4_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "Bd_Pw_Bat_sp_out": {
        "type": "scalar",
        "lower_bound": -1,
        "upper_bound": 1,
    },
    "Bd_Ch_EVBat_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Bd_DisCh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Bd_Frac_Vent_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Z01_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z02_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z03_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z04_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z05_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z06_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z07_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "Z08_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
    },
    "P1_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "P2_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "P3_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "P4_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Z01_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z01_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z02_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z02_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z03_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z03_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z04_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z04_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z05_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z05_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z06_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z06_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z07_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z07_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Z08_T": {"type": "scalar", "lower_bound": 10, "upper_bound": 40},
    "Z08_RH": {"type": "scalar", "lower_bound": 0, "upper_bound": 100},
    "Fa_Stat_EV": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Fa_ECh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
    },
    "Fa_EDCh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
    },
    "Fa_ECh_Bat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
    },
    "Fa_EDCh_Bat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
    },
    "Bd_FracCh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Bd_FracCh_Bat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "P4_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "P2_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "P1_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "P3_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
    },
    "HVAC_Pw_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 12e4,
    },
    "HVAC_onoff_HP_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "HVAC_onoff_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
    },
    "Bd_E_HW": {
        "type": "scalar",
        "lower_bound": -3e3,
        "upper_bound": 3e3,
    },
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e4,
    },
    "Fa_Pw_Prod": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
    },
    "Fa_E_self": {
        "type": "scalar",
        "lower_bound": -2e3,
        "upper_bound": 2e3,
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e3,
    },
    "Fa_E_All": {"type": "scalar", "lower_bound": 0, "upper_bound": 2e3},
    "Fa_E_Light": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
    },
    "Fa_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 5e2,
    },
}

default_kpi_options = {
    "kpi1": {"name": "Fa_E_self", "type": "avg"},
    "kpi2": {"name": "Z01_T", "type": "avg_dev", "target": [19, 24]},
    "kpi3": {"name": "Z02_T", "type": "avg_dev", "target": [19, 24]},
    "kpi4": {"name": "Z03_T", "type": "avg_dev", "target": [19, 24]},
    "kpi5": {"name": "Z04_T", "type": "avg_dev", "target": [19, 24]},
    "kpi6": {"name": "Z05_T", "type": "avg_dev", "target": [19, 24]},
    "kpi7": {"name": "Z06_T", "type": "avg_dev", "target": [19, 24]},
    "kpi8": {"name": "Z07_T", "type": "avg_dev", "target": [19, 24]},
    "kpi9": {"name": "Z08_T", "type": "avg_dev", "target": [19, 24]},
    "kpi10": {"name": "Z01_T", "type": "tot_viol", "target": [19, 24]},
    "kpi11": {"name": "Z02_T", "type": "tot_viol", "target": [19, 24]},
    "kpi12": {"name": "Z03_T", "type": "tot_viol", "target": [19, 24]},
    "kpi13": {"name": "Z04_T", "type": "tot_viol", "target": [19, 24]},
    "kpi14": {"name": "Z05_T", "type": "tot_viol", "target": [19, 24]},
    "kpi15": {"name": "Z06_T", "type": "tot_viol", "target": [19, 24]},
    "kpi16": {"name": "Z07_T", "type": "tot_viol", "target": [19, 24]},
    "kpi17": {"name": "Z08_T", "type": "tot_viol", "target": [19, 24]},
}


class Seilab(EnvEPlusFMU):
    """Containing information for the models SeilabThermal-v0 and SeilabGrid-v0.

    Subclasses EnvEPlusFMU and inherits its behavior. Simulation based details are
    specified in this class and passed to the constructor of EnvEPlusFMU.

    Attributes
    -----------
    EV_schedule : ElectricVehicleSchedule
        Energy consumption schedule for electric vehicles

    Methods
    --------
    step(inputs):
        Advances the simulation one timestep.
    predict_ev(steps):
        Provides a forecast for the EV schedule.
    """

    def __init__(
        self,
        model_path,
        EV_schedule,
        start_day=1,
        start_month=1,
        year=2019,
        simulation_days=10,
        weather="ESP_CT_Barcelona",
        kpi_options=None,
        default_path=True,
        generate_forecasts=True,
        generate_forecast_method="perfect",
        generate_forecast_keys=None,
    ):
        """
        Parameters
        ----------
        model_path : str
            Specifies the path to the FMU
        EV_schedule : ElectricVehicleSchedule
            Energy consumption schedule for electric vehicles
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
            "ESP_CT_Barcelona"
        kpi_options : dict, optional
            Dict to specify the tracked KPIs, by default None.
        """

        n_steps = 20
        step_size = 3 * 60
        start_date = datetime.date(year, start_month, start_day)
        delta = start_date - datetime.date(year, 1, 1)
        start_time = delta.total_seconds()
        stop_time = (
            start_time + n_steps * 24 * simulation_days * step_size
        )
        if kpi_options is None:
            kpi_options = default_kpi_options

        self.EV_schedule = EV_schedule

        super().__init__(
            model_path,
            start_time,
            stop_time,
            step_size,
            weather,
            INPUTS_SPECS,
            OUTPUTS_SPECS,
            kpi_options,
            default_path,
            generate_forecasts,
            generate_forecast_method,
            generate_forecast_keys,
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
        ev_val = self.EV_schedule.get(date)
        inputs["Bd_DisCh_EVBat_sp"] = [ev_val]
        out = super().step(inputs=inputs)
        return out

    def predict_ev(self, steps):
        """Provides a forecast for the EV schedule.

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
            predictions.append(self.EV_schedule.predict(date))
            date = date + datetime.timedelta(minutes=3)
        return {"Bd_DisCh_EVBat": predictions}

    def get_forecast(self, forecast_length=24, **kwargs):
        forecasts = super().get_forecast(forecast_length, **kwargs)
        predictions = self.predict_ev(steps=forecast_length)
        forecasts = {**forecasts, **predictions}
        return forecasts
