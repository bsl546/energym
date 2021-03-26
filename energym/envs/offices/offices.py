import datetime

from energym.envs.env_fmu_eplus import EnvEPlusFMU


INPUTS_SPECS = {
    "Bd_Cooling_onoff_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "",
    },
    "Bd_Heating_onoff_sp": {
        "type": "discrete",
        "size": 2,
        "default": 1,
        "description": "",
    },
    "Z01_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z02_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z03_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z04_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z05_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z06_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z07_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z15_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z16_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z17_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z18_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z19_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z20_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
    "Z25_T_Thermostat_sp": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "default": 20,
        "description": "",
    },
}

OUTPUTS_SPECS = {
    "Bd_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 5000,
        "description": "",
    },
    "Ext_Irr": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "",
    },
    "Ext_RH": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "",
    },
    "Ext_T": {
        "type": "scalar",
        "lower_bound": -10,
        "upper_bound": 40,
        "description": "",
    },
    "Fa_Pw_All": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
        "description": "",
    },
    "Fa_Pw_HVAC": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1e4,
        "description": "",
    },
    "Fa_Pw_PV": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 2e3,
        "description": "",
    },
    "Z01_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z01_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z01_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z02_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z02_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z02_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z03_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z03_Fl_Fan1_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z03_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z03_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z04_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z04_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z04_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z05_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z05_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z05_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z06_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z06_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z06_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z07_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z07_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z07_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z15_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z15_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z15_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z16_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z16_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z16_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z17_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z17_Fl_Fan1_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z17_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z17_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z18_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z18_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z18_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z19_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z19_Fl_Fan1_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z19_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z19_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z20_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z20_Fl_Fan1_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z20_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z20_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
    "Z25_Fl_Fan_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z25_Fl_Fan1_sp_out": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "",
    },
    "Z25_T": {
        "type": "scalar",
        "lower_bound": 10,
        "upper_bound": 40,
        "description": "",
    },
    "Z25_T_Thermostat_sp_out": {
        "type": "scalar",
        "lower_bound": 16,
        "upper_bound": 26,
        "description": "",
    },
}

default_kpi_options = {
    "kpi1": {"name": "Fa_Pw_All", "type": "avg"},
    "kpi2": {"name": "Z01_T", "type": "avg_dev", "target": [19, 24]},
    "kpi3": {"name": "Z02_T", "type": "avg_dev", "target": [19, 24]},
    "kpi4": {"name": "Z03_T", "type": "avg_dev", "target": [19, 24]},
    "kpi5": {"name": "Z04_T", "type": "avg_dev", "target": [19, 24]},
    "kpi6": {"name": "Z05_T", "type": "avg_dev", "target": [19, 24]},
    "kpi7": {"name": "Z06_T", "type": "avg_dev", "target": [19, 24]},
    "kpi8": {"name": "Z07_T", "type": "avg_dev", "target": [19, 24]},
    "kpi16": {"name": "Z15_T", "type": "avg_dev", "target": [19, 24]},
    "kpi17": {"name": "Z16_T", "type": "avg_dev", "target": [19, 24]},
    "kpi18": {"name": "Z17_T", "type": "avg_dev", "target": [19, 24]},
    "kpi19": {"name": "Z18_T", "type": "avg_dev", "target": [19, 24]},
    "kpi20": {"name": "Z19_T", "type": "avg_dev", "target": [19, 24]},
    "kpi21": {"name": "Z20_T", "type": "avg_dev", "target": [19, 24]},
    "kpi26": {"name": "Z25_T", "type": "avg_dev", "target": [19, 24]},
    "kpi27": {"name": "Z01_T", "type": "tot_viol", "target": [19, 24]},
    "kpi28": {"name": "Z02_T", "type": "tot_viol", "target": [19, 24]},
    "kpi29": {"name": "Z03_T", "type": "tot_viol", "target": [19, 24]},
    "kpi30": {"name": "Z04_T", "type": "tot_viol", "target": [19, 24]},
    "kpi31": {"name": "Z05_T", "type": "tot_viol", "target": [19, 24]},
    "kpi32": {"name": "Z06_T", "type": "tot_viol", "target": [19, 24]},
    "kpi33": {"name": "Z07_T", "type": "tot_viol", "target": [19, 24]},
    "kpi41": {"name": "Z15_T", "type": "tot_viol", "target": [19, 24]},
    "kpi42": {"name": "Z16_T", "type": "tot_viol", "target": [19, 24]},
    "kpi43": {"name": "Z17_T", "type": "tot_viol", "target": [19, 24]},
    "kpi44": {"name": "Z18_T", "type": "tot_viol", "target": [19, 24]},
    "kpi45": {"name": "Z19_T", "type": "tot_viol", "target": [19, 24]},
    "kpi46": {"name": "Z20_T", "type": "tot_viol", "target": [19, 24]},
    "kpi51": {"name": "Z25_T", "type": "tot_viol", "target": [19, 24]},
}


class Offices(EnvEPlusFMU):
    """Containing information for the model OfficesThermostat-v0.

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
