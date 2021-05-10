import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU


INPUTS_SPECS = {
    "Z02_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 2 thermostat setpoint (°C).",
    },
    "Z03_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 3 thermostat setpoint (°C).",
    },
    "Z04_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 4 thermostat setpoint (°C).",
    },
    "Z05_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 5 thermostat setpoint (°C).",
    },
    "Z08_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 8 thermostat setpoint (°C).",
    },
    "Z09_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 9 thermostat setpoint (°C).",
    },
    "Z10_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 10 thermostat setpoint (°C).",
    },
    "Z11_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 11 thermostat setpoint (°C).",
    },
    "Bd_T_AHU2_sp": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 30,
        "default": 20,
        "description": "AHU 2 temperature setpoint (°C).",
    },
    "Bd_Fl_AHU2_sp": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "default": 1,
        "description": "AHU 2 flow rate setpoint.",
    },
    "Bd_T_AHU1_sp": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 30,
        "default": 20,
        "description": "AHU 1 temperature setpoint (°C).",
    },
    "Bd_Fl_AHU1_sp": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "default": 1,
        "description": "AHU1 flow rate setpoint.",
    },
}

OUTPUTS_SPECS = {
    "Bd_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
        "description": "Building power consumption (W).",
    },
    "Bd_Pw_chiller": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e4,
        "description": "Chiller power consumption (W).",
    },
    "Bd_Pw_coil": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1.5e4,
        "description": "Heating coil power consumption (W).",
    },
    "Bd_Pw_cooling_AHU2": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
        "description": "AHU 2 cooling power (W).",
    },
    "Bd_Pw_cooling_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e4,
        "description": "Heat pump cooling power (W).",
    },
    "Bd_Pw_heating_HP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e4,
        "description": "Heat pump heating power (W).",
    },
    "Bd_T_AHU1": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 30,
        "description": "AHU 1 temperature (°C).",
    },
    "Bd_T_AHU2": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 30,
        "description": "AHU 2 temperature (°C).",
    },
    "Ext_Irr": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "Ext_P": {
        "type": "scalar",
        "lower_bound": 8e4,
        "upper_bound": 13e4,
        "description": "Outdoor air pressure (Pa).",
    },
    "Ext_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Outdoor realtive humidity (%RH).",
    },
    "Ext_T": {
        "type": "scalar",
        "lower_bound": -10,
        "upper_bound": 40,
        "description": "Outdoor temperature (°C).",
    },
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 5e4,
        "description": "Total power consumtion (W).",
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 5e4,
        "description": "HVAC power consumption (W).",
    },
    "Z02_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 2 fan flow rate.",
    },
    "Z02_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 2 relative humidity (%RH).",
    },
    "Z02_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 2 temperature (°C).",
    },
    "Z02_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 2 thermostat setpoint (°C).",
    },
    "Z03_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 3 fan flow rate.",
    },
    "Z03_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 3 relative humidity (%RH).",
    },
    "Z03_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 3 temperature (°C).",
    },
    "Z03_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 3 thermostat setpoint (°C).",
    },
    "Z04_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 4 fan flow rate.",
    },
    "Z04_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 4 relative humidity (%RH).",
    },
    "Z04_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 4 temperature (°C).",
    },
    "Z04_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 4 thermostat setpoint (°C).",
    },
    "Z05_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 5 relative humidity (%RH).",
    },
    "Z05_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 5 temperature (°C).",
    },
    "Z05_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 5 thermostat setpoint (°C).",
    },
    "Z08_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 8 fan flow rate.",
    },
    "Z08_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 8 relative humidity (%RH).",
    },
    "Z08_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 8 temperature (°C).",
    },
    "Z08_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 8 thermostat setpoint (°C).",
    },
    "Z09_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 9 fan flow rate.",
    },
    "Z09_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 9 relative humidity (%RH).",
    },
    "Z09_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 9 temperature (°C).",
    },
    "Z09_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 9 thermostat setpoint (°C).",
    },
    "Z10_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 10 fan flow rate.",
    },
    "Z10_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 10 relative humidity (%RH).",
    },
    "Z10_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 10 temperature (°C).",
    },
    "Z10_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 10 thermostat setpoint (°C).",
    },
    "Z11_Fl_Fan": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "Zone 11 fan flow rate.",
    },
    "Z11_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 11 relative humidity (%RH).",
    },
    "Z11_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 11 temperature (°C).",
    },
    "Z11_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 11 thermostat setpoint (°C).",
    },
}

default_kpi_options = {
    "kpi1": {"name": "Fa_Pw_All", "type": "avg"},
    "kpi2": {"name": "Z02_T", "type": "avg_dev", "target": [19, 24]},
    "kpi3": {"name": "Z03_T", "type": "avg_dev", "target": [19, 24]},
    "kpi4": {"name": "Z04_T", "type": "avg_dev", "target": [19, 24]},
    "kpi5": {"name": "Z05_T", "type": "avg_dev", "target": [19, 24]},
    "kpi6": {"name": "Z08_T", "type": "avg_dev", "target": [19, 24]},
    "kpi7": {"name": "Z09_T", "type": "avg_dev", "target": [19, 24]},
    "kpi8": {"name": "Z10_T", "type": "avg_dev", "target": [19, 24]},
    "kpi9": {"name": "Z11_T", "type": "avg_dev", "target": [19, 24]},
    "kpi10": {"name": "Z02_T", "type": "tot_viol", "target": [19, 24]},
    "kpi11": {"name": "Z03_T", "type": "tot_viol", "target": [19, 24]},
    "kpi12": {"name": "Z04_T", "type": "tot_viol", "target": [19, 24]},
    "kpi13": {"name": "Z05_T", "type": "tot_viol", "target": [19, 24]},
    "kpi14": {"name": "Z08_T", "type": "tot_viol", "target": [19, 24]},
    "kpi15": {"name": "Z09_T", "type": "tot_viol", "target": [19, 24]},
    "kpi16": {"name": "Z10_T", "type": "tot_viol", "target": [19, 24]},
    "kpi17": {"name": "Z11_T", "type": "tot_viol", "target": [19, 24]},
}


class MixedUse(EnvEPlusFMU):
    """Containing information for the model MixedUseFanFCU-v0.

    Subclasses EnvEPlusFMU and inherits its behavior. Simulation based details are
    specified in this class and passed to the constructor of EnvEPlusFMU.
    """

    def __init__(
        self,
        model_path,
        start_day=1,
        start_month=1,
        year=2019,
        simulation_days=10,
        weather="GRC_A_Athens",
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
            "GRC_A_Athens"
        kpi_options : dict, optional
            Dict to specify the tracked KPIs, by default None.
        """

        n_steps = 4
        step_size = 15 * 60
        start_date = datetime.date(year, start_month, start_day)
        delta = start_date - datetime.date(year, 1, 1)
        start_time = delta.total_seconds()
        stop_time = start_time + n_steps * 24 * simulation_days * step_size
        if kpi_options is None:
            kpi_options = default_kpi_options

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
