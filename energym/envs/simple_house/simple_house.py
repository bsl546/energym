import datetime
from energym.envs.env_fmu_mod import EnvModFMU

INPUTS_SPECS = {
    "u": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1,
        "default": 0,
        "description": "Heat pump power fraction setpoint.",
    }
}

OUTPUTS_SPECS_RAD = {
    "weaBus.HDifHor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal diffuse solar radiation (W/m2).",
    },
    "weaBus.HDirNor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "weaBus.HGloHor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal global radiation (W/m2).",
    },
    "weaBus.HHorIR": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal infrared radiation (W/m2).",
    },
    "sunRad.y": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "sunHea.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Solar heat flow rate (W).",
    },
    "preHea.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Prescribed heat flow rate (W).",
    },
    "heaPum.P": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Heat pump consumed power (W).",
    },
    "heaPum.QCon_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Actual heating heat flow rate added to fluid (W).",
    },
    "heaPum.QEva_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Actual cooling heat flow rate removed from fluid (W).",
    },
    "heaPum.COP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 20,
        "description": "Heat pump coefficient of performance.",
    },
    "heaPum.COPCar": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 20,
        "description": "Heat pump carnot efficiency.",
    },
    "heaPum.TConAct": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Condenser temperature used to compute efficiency (K).",
    },
    "heaPum.TEvaAct": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Evaporator temperature used to compute efficiency (K).",
    },
    "rad.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Radiator heat flow rate (W).",
    },
    "rad.m_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 10,
        "description": "Radiator mass flow rate (kg/s).",
    },
    "temRet.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 353.15,
        "description": "Heat pump return temperature (K).",
    },
    "temSup.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 353.15,
        "description": "Heat pump supply temperature (K).",
    },
    "TOut.T": {
        "type": "scalar",
        "lower_bound": 253.15,
        "upper_bound": 343.15,
        "description": "Outdoor temperature (K).",
    },
    "temRoo.T": {
        "type": "scalar",
        "lower_bound": 263.15,
        "upper_bound": 343.15,
        "description": "Indoor temperature (K).",
    },
    "y": {
        "type": "scalar",
        "lower_bound": 263.15,
        "upper_bound": 343.15,
        "description": "Indoor temperature (K).",
    },
}

OUTPUTS_SPECS_SLAB = {
    "weaBus.HDifHor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal diffuse solar radiation (W/m2).",
    },
    "weaBus.HDirNor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "weaBus.HGloHor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal global radiation (W/m2).",
    },
    "weaBus.HHorIR": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal infrared radiation (W/m2).",
    },
    "sunRad.y": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "sunHea.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Solar heat flow rate (W).",
    },
    "preHea.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Prescribed heat flow rate (W).",
    },
    "heaPum.P": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Heat pump consumed power (W).",
    },
    "heaPum.QCon_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Actual heating heat flow rate added to fluid (W).",
    },
    "heaPum.QEva_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Actual cooling heat flow rate removed from fluid (W).",
    },
    "heaPum.COP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 20,
        "description": "Heat pump coefficient of performance.",
    },
    "heaPum.COPCar": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 20,
        "description": "Heat pump Carnot efficiency.",
    },
    "heaPum.TConAct": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Condenser temperature used to compute efficiency (K).",
    },
    "heaPum.TEvaAct": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Evaporator temperature used to compute efficiency (K).",
    },
    "sla.surf_a.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Slab heat flow rate (W).",
    },
    "sla.surf_b.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Slab heat flow rate (W).",
    },
    "sla.m_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 10,
        "description": "Slab mass flow rate (kg/s).",
    },
    "sla.surf_a.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Slab temperature (K).",
    },
    "sla.surf_b.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Slab temperature (K).",
    },
    "temRet.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 353.15,
        "description": "Heat pump return temperature (K).",
    },
    "temSup.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 353.15,
        "description": "Heat pump supply temperature (K).",
    },
    "TOut.T": {
        "type": "scalar",
        "lower_bound": 253.15,
        "upper_bound": 343.15,
        "description": "Outdoor temperature (K).",
    },
    "temRoo.T": {
        "type": "scalar",
        "lower_bound": 263.15,
        "upper_bound": 343.15,
        "description": "Indoor temperature (K).",
    },
    "y": {
        "type": "scalar",
        "lower_bound": 263.15,
        "upper_bound": 343.15,
        "description": "Indoor temperature (K).",
    },
}

OUTPUTS_SPECS_RSLA = {
    "weaBus.HDifHor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal diffuse solar radiation (W/m2).",
    },
    "weaBus.HDirNor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "weaBus.HGloHor": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal global radiation (W/m2).",
    },
    "weaBus.HHorIR": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Horizontal infrared radiation (W/m2).",
    },
    "sunRad.y": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 1000,
        "description": "Direct normal radiation (W/m2).",
    },
    "sunHea.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Solar heat flow rate (W).",
    },
    "preHea.Q_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Prescribed heat flow rate (W).",
    },
    "heaPum.P": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Heat pump consumed power (W).",
    },
    "heaPum.QCon_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Actual heating heat flow rate added to fluid (W).",
    },
    "heaPum.QEva_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Actual cooling heat flow rate removed from fluid (W).",
    },
    "heaPum.COP": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 20,
        "description": "Heat pump coefficient of performance.",
    },
    "heaPum.COPCar": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 20,
        "description": "Heat pump Carnot efficiency.",
    },
    "heaPum.TConAct": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Condenser temperature used to compute efficiency (K).",
    },
    "heaPum.TEvaAct": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Evaporator temperature used to compute efficiency (K).",
    },
    "sla.QTot": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 100,
        "description": "Slab heat flow rate (W).",
    },
    "sla.m_flow": {
        "type": "scalar",
        "lower_bound": 0,
        "upper_bound": 10,
        "description": "Slab mass flow rate (kg/s).",
    },
    "sla.heatPortEmb[1].T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 343.15,
        "description": "Slab temperature (K).",
    },
    "temRet.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 353.15,
        "description": "Heat pump return temperature (K).",
    },
    "temSup.T": {
        "type": "scalar",
        "lower_bound": 273.15,
        "upper_bound": 353.15,
        "description": "Heat pump supply temperature (K).",
    },
    "TOut.T": {
        "type": "scalar",
        "lower_bound": 253.15,
        "upper_bound": 343.15,
        "description": "Outdoor temperature (K).",
    },
    "temRoo.T": {
        "type": "scalar",
        "lower_bound": 263.15,
        "upper_bound": 343.15,
        "description": "Indoor temperature (K).",
    },
    "y": {
        "type": "scalar",
        "lower_bound": 263.15,
        "upper_bound": 343.15,
        "description": "Indoor temperature (K).",
    },
}

default_kpi_options = {
    "kpi1": {"name": "heaPum.P", "type": "avg"},
    "kpi2": {
        "name": "temRoo.T",
        "type": "avg_dev",
        "target": [292.15, 297.15],
    },
    "kpi3": {
        "name": "temRoo.T",
        "type": "tot_viol",
        "target": [292.15, 297.15],
    },
}


class SimpleHouse(EnvModFMU):
    """Containing information for the models

    Subclasses EnvModFMU and inherits its behavior. Simulation based details are
    specified in this class and passed to the constructor of EnvModFMU.
    """

    def __init__(
        self,
        model_path,
        start_day=1,
        start_month=1,
        year=2019,
        simulation_days=21,
        weather="CH_BS_Basel",
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
            "CH_ZH_Maur"
        kpi_options : dict, optional
            Dict to specify the tracked KPIs, by default None.
        """
        n_steps = 12
        step_size = 5 * 60
        start_date = datetime.date(year, start_month, start_day)
        delta = start_date - datetime.date(year, 1, 1)
        start_time = delta.total_seconds()
        stop_time = start_time + n_steps * 24 * simulation_days * step_size
        params = {
            "P_nominal": 5e3,
            "COP_nominal": 5.0,
            "therm_cond_G": 500.0,
            "heat_capa_C": 1e7,
            "QRooInt_flow": 700.0,
        }
        init_vals = {"u": 0.0}

        if kpi_options is None:
            kpi_options = default_kpi_options

        if "Rad" in model_path:
            outputs_specs = OUTPUTS_SPECS_RAD
        elif "Slab" in model_path:
            outputs_specs = OUTPUTS_SPECS_SLAB
        else:
            outputs_specs = OUTPUTS_SPECS_RSLA

        super().__init__(
            model_path,
            start_time,
            stop_time,
            step_size,
            weather,
            params,
            init_vals,
            INPUTS_SPECS,
            outputs_specs,
            kpi_options,
            default_path,
            generate_forecasts,
            generate_forecast_method,
            generate_forecast_keys,
        )
