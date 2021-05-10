import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU
from energym.schedules.EProductionSchedule import EProductionSchedule


INPUTS_SPECS = {
    "Bd_onoff_HP1_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "Heat pump 1 on/off setpoint.",
    },
    "Bd_onoff_HP2_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "Heat pump 2 on/off setpoint.",
    },
    "Bd_onoff_HP3_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "Heat pump 3 on/off setpoint.",
    },
    "Bd_onoff_HP4_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "Heat pump 4 on/off setpoint.",
    },
    "Bd_T_HP1_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
        "description": "Heat pump 1 temperature setpoint (°C).",
    },
    "Bd_T_HP2_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
        "description": "Heat pump 2 temperature setpoint (°C).",
    },
    "Bd_T_HP3_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
        "description": "Heat pump 3 temperature setpoint (°C).",
    },
    "Bd_T_HP4_sp": {
        "type": "scalar",
        "lower_bound": 30,
        "upper_bound": 65,
        "default": 50,
        "description": "Heat pump 4 temperature setpoint (°C).",
    },
    "Bd_T_AHU_coil_sp": {
        "type": "scalar",
        "lower_bound": 15,
        "upper_bound": 40,
        "default": 30,
        "description": "AHU temperature setpoint (°C).",
    },
    "Bd_T_buffer_sp": {
        "type": "scalar",
        "lower_bound": 15,
        "upper_bound": 70,
        "default": 40,
        "description": "Buffer tank temperature setpoint (°C).",
    },
    "Bd_T_mixer_sp": {
        "type": "scalar",
        "lower_bound": 20,
        "upper_bound": 60,
        "default": 40,
        "description": "Mixer temperature setpoint (°C).",
    },
    "Bd_T_Boiler_sp": {
        "type": "scalar",
        "lower_bound": 20,
        "upper_bound": 80,
        "default": 40,
        "description": "Gas boiler temperature setpoint (°C).",
    },
    "Bd_T_HVAC_sp": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 26,
        "default": 20,
        "description": "HVAC temperature setpoint (°C).",
    },
    "Z01_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 1 thermostat setpoint (°C).",
    },
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
    "Z06_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 6 thermostat setpoint (°C).",
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
    "Z13_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 13 thermostat setpoint (°C).",
    },
    "Z14_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 14 thermostat setpoint (°C).",
    },
    "Z15_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 15 thermostat setpoint (°C).",
    },
    "Z18_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 18 thermostat setpoint (°C).",
    },
    "Z19_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 19 thermostat setpoint (°C).",
    },
    "Z20_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 20 thermostat setpoint (°C).",
    },
    "Z21_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 21 thermostat setpoint (°C).",
    },
    "Z22_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "Zone 22 thermostat setpoint (°C).",
    },
}


OUTPUTS_SPECS = {
    "Bd_T_Boiler_sp_out": {
        "type": "scalar",
        "lower_bound": 20,
        "upper_bound": 80,
        "description": "Gas boiler temperature setpoint (°C).",
    },
    "Bd_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
        "description": "Building power consumption (W).",
    },
    "Bd_Pw_prod": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
        "description": "PV power production (W).",
    },
    "Bd_Pw_boiler": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 3e5,
        "description": "Gas boiler power consumption (W).",
    },
    "Ext_Irr": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "Ext_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Outdoor relative humidity (%RH).",
    },
    "Ext_T": {
        "type": "scalar",
        "lower_bound": -15,
        "upper_bound": 40,
        "description": "Outdoor temperature (°C).",
    },
    "Ext_P": {
        "type": "scalar",
        "lower_bound": 80000,
        "upper_bound": 130000,
        "description": "Outdoor air pressure (Pa).",
    },
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
        "description": "Total power consumption (W).",
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
        "description": "HVAC power consumption (W).",
    },
    "Fa_Pw_Pur": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e5,
        "description": "Purchased power (W).",
    },
    "Z01_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 1 relative humidity (%RH).",
    },
    "Z01_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 1 temperature (°C).",
    },
    "Z01_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 1 thermostat setpoint (°C).",
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
    "Z06_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 6 relative humidity (%RH).",
    },
    "Z06_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 6 temperature (°C).",
    },
    "Z06_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 6 thermostat setpoint (°C).",
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
    "Z13_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 12 relative humidity (%RH).",
    },
    "Z13_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 13 temperature (°C).",
    },
    "Z13_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 13 thermostat setpoint (°C).",
    },
    "Z14_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 14 relative humidity (%RH).",
    },
    "Z14_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 14 temperature (°C).",
    },
    "Z14_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 14 thermostat setpoint (°C).",
    },
    "Z15_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 15 relative humidity (%RH).",
    },
    "Z15_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 15 temperature (°C).",
    },
    "Z15_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 15 thermostat setpoint (°C).",
    },
    "Z18_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 18 relative humidity (%RH).",
    },
    "Z18_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 18 temperature (°C).",
    },
    "Z18_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 18 thermostat setpoint (°C).",
    },
    "Z19_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 19 relative humidity (%RH).",
    },
    "Z19_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 19 temperature (°C).",
    },
    "Z19_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 19 thermostat setpoint (°C).",
    },
    "Z20_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 20 relative humidity (%RH).",
    },
    "Z20_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 20 temperature (°C).",
    },
    "Z20_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 20 thermostat setpoint (°C).",
    },
    "Z21_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 21 relative humidity (%RH).",
    },
    "Z21_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 21 temperature (°C).",
    },
    "Z21_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 21 thermostat setpoint (°C).",
    },
    "Z22_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Zone 22 relative humidity (%RH).",
    },
    "Z22_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "Zone 22 temperature (°C).",
    },
    "Z22_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "Zone 22 thermostat setpoint (°C).",
    },
    "Bd_CO2": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 10,
        "description": "Building CO2 emission.",
    },
    "Grid_CO2": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e3,
        "description": "Grid CO2 emission.",
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
        stop_time = start_time + n_steps * 24 * simulation_days * step_size
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
