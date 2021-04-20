import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU

INPUTS_SPECS = {
    "P1_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Floor 1 thermostat setpoint (°C).",
    },
    "P2_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Floor 2 thermostat setpoint (°C).",
    },
    "P3_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Floor 3 thermostat setpoint (°C).",
    },
    "P4_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Floor 4 thermostat setpoint (°C).",
    },
    "Bd_T_HP_sp": {
        "type": "scalar",
        "lower_bound": 35,
        "upper_bound": 55,
        "default": 45,
        "description": "Heat pump temperature setpoint (°C).",
    },
    "P1_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
        "description": "Floor 1 tank temperature setpoint (°C).",
    },
    "P2_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
        "description": "Floor 2 tank temperature setpoint (°C).",
    },
    "P3_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
        "description": "Floor 3 tank temperature setpoint (°C).",
    },
    "P4_T_Tank_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "default": 50,
        "description": "Floor 4 tank temperature setpoint (°C).",
    },
    "HVAC_onoff_HP_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "Heat pump on/off setpoint",
    },
    "Bd_Pw_Bat_sp": {
        "type": "scalar",
        "lower_bound": -1,
        "upper_bound": 1,
        "default": 0,
        "description": "Battery charging/discharging setpoint rate.",
    },
    "Bd_Ch_EVBat_sp": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "default": 0,
        "description": "EV battery charging setpoint rate.",
    },
}


OUTPUTS_SPECS = {
    "Ext_T": {
        "type": "scalar",
        "lower_bound": -10,
        "upper_bound": 40,
        "description": "Outdoor temperature (°C).",
    },
    "Ext_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Outdoor relative humidity (%RH).",
    },
    "Ext_Irr": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2)",
    },
    "Ext_P": {
        "type": "scalar",
        "lower_bound": 80000,
        "upper_bound": 130000,
        "description": "Outdoor air pressure (Pa).",
    },
    "P3_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Floor 3 thermostat setpoint (°C).",
    },
    "P4_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Floor 4 thermostat setpoint (°C).",
    },
    "P2_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Floor 2 thermostat setpoint (°C).",
    },
    "P1_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Floor 1 thermostat setpoint (°C).",
    },
    "Bd_Fl_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2,
        "description": "Heat pump flow rate (kg/s).",
    },
    "Bd_T_HP_return": {
        "type": "scalar",
        "lower_bound": 35,
        "upper_bound": 55,
        "description": "Heat pump return temperature (°C).",
    },
    "Bd_T_HP_supply": {
        "type": "scalar",
        "lower_bound": 35,
        "upper_bound": 55,
        "description": "Heat pump supply temperature (°C).",
    },
    "Bd_T_HP_sp_out": {
        "type": "scalar",
        "lower_bound": 35,
        "upper_bound": 55,
        "description": "Heat pump temperature setpoint (°C).",
    },
    "P1_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 1 temperature setpoint (°C).",
    },
    "P2_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 2 temperature setpoint (°C).",
    },
    "P3_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 3 temperature setpoint (°C).",
    },
    "P4_T_Tank_sp_out": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 4 temperature setpoint (°C).",
    },
    "Bd_Pw_Bat_sp_out": {
        "type": "scalar",
        "lower_bound": -1,
        "upper_bound": 1,
        "description": "Battery charging/discharging rate setpoint.",
    },
    "Bd_Ch_EVBat_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "EV battery charging rate setpoint .",
    },
    "Bd_DisCh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "EV battery discharging rate.",
    },
    "Bd_Frac_Vent_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Ventilation power fraction.",
    },
    "Z01_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 1 appliance energy (Wh).",
    },
    "Z02_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 2 appliance energy (Wh).",
    },
    "Z03_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 3 appliance energy (Wh).",
    },
    "Z04_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 4 appliance energy (Wh).",
    },
    "Z05_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 5 appliance energy (Wh).",
    },
    "Z06_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 6 appliance energy (Wh).",
    },
    "Z07_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 7 appliance energy (Wh).",
    },
    "Z08_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Zone 8 appliance energy (Wh).",
    },
    "P1_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Floor 1 hot water flow rate fraction.",
    },
    "P2_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Floor 2 hot water flow rate fraction.",
    },
    "P3_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Floor 3 hot water flow rate fraction.",
    },
    "P4_FlFrac_HW": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Floor 4 hot water flow rate fraction.",
    },
    "Z01_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 1 temperature (°C).",
    },
    "Z01_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 1 relative humidity (%RH).",
    },
    "Z02_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 2 temperature (°C).",
    },
    "Z02_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 2 relative humidity (%RH).",
    },
    "Z03_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 3 temperature (°C).",
    },
    "Z03_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 3 relative humidity (%RH).",
    },
    "Z04_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 4 temperature (°C).",
    },
    "Z04_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 4 relative humidity (%RH).",
    },
    "Z05_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 5 temperature (°C).",
    },
    "Z05_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 5 relative humidity (%RH).",
    },
    "Z06_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 6 temperature (°C).",
    },
    "Z06_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 6 relative humidity (%RH).",
    },
    "Z07_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 7 temperature (°C).",
    },
    "Z07_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 7 relative humidity (%RH).",
    },
    "Z08_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 8 temperature (°C).",
    },
    "Z08_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 8 relative humidity (%RH).",
    },
    "Fa_Stat_EV": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "EV status (availability)",
    },
    "Fa_ECh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
        "description": "EV battery charging energy (Wh).",
    },
    "Fa_EDCh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
        "description": "EV battery discharging energy (Wh).",
    },
    "Fa_ECh_Bat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
        "description": "Battery charging energy (Wh).",
    },
    "Fa_EDCh_Bat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 4e3,
        "description": "Battery discharging energy (Wh).",
    },
    "Bd_FracCh_EVBat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "EV battery state of charge.",
    },
    "Bd_FracCh_Bat": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Battery state of charge.",
    },
    "P4_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 4 tank temperature (°C).",
    },
    "P2_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 2 tank temperature (°C).",
    },
    "P1_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 1 tank temperature (°C).",
    },
    "P3_T_Tank": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 70,
        "description": "Floor 3 tank temperature (°C).",
    },
    "HVAC_Pw_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 12e4,
        "description": "Heat pump power (W)",
    },
    "HVAC_onoff_HP_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Heat pump on/off setpoint.",
    },
    "HVAC_onoff_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Heat pump on/off status.",
    },
    "Bd_E_HW": {
        "type": "scalar",
        "lower_bound": -3e3,
        "upper_bound": 3e3,
        "description": "Hot water energy (Wh).",
    },
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e4,
        "description": "Total power consumption (W).",
    },
    "Fa_Pw_Prod": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
        "description": "PV power production (W).",
    },
    "Fa_E_self": {
        "type": "scalar",
        "lower_bound": -2e3,
        "upper_bound": 2e3,
        "description": "Self consumption energy (Wh).",
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e3,
        "description": "HVAC energy consumption (Wh).",
    },
    "Fa_E_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e3,
        "description": "Total energy consumption (Wh).",
    },
    "Fa_E_Light": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Lighting energy (Wh).",
    },
    "Fa_E_Appl": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 5e2,
        "description": "Appliances energy (Wh).",
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


class Apartments(EnvEPlusFMU):
    """Containing information for the models ApartmentsThermal-v0 and ApartmentsGrid-v0.

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
        stop_time = start_time + n_steps * 24 * simulation_days * step_size
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
