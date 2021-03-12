import os
import platform
import pandas as pd
import datetime

from energym.envs.env_names import EnvNames
from energym.envs.irec_seilab.seilab import Seilab
from energym.envs.irec_smartlab.smartlab import Smartlab
from energym.envs.datacenter.datacenter import DataCenter
from energym.envs.offices.offices import Offices
from energym.envs.silo.silo import Silo
from energym.envs.seminarcenter.seminarcenter import Seminarcenter
from energym.envs.simple_house.simple_house import SimpleHouse
from energym.envs.swiss_house.swiss_house import SwissHouse
from energym.schedules.CPUSchedule import CPUSchedule
from energym.schedules.EProductionSchedule import EProductionSchedule
from energym.schedules.EVSchedule import ElectricVehicleSchedule


def make(key, eval_mode=False, **kwargs):
    """Creates an instance of the requested simulation model.

    Parameters
    ----------
    key : str
        Name of the simulation model.
    eval_mode : bool
        Whether to return an instance of the evaluation scenario

    Returns
    -------
    Simulation model object
        The instantiation of the corresponding simulation model.

    Raises
    ------
    Exception
        If the requested model is not available or the configuration is
        not correct.
    """
    op_sys = platform.system().lower()
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if key == EnvNames.SEILAB_THERMAL_V0.value:
        ev_schedule = ElectricVehicleSchedule(30, 50, 37 / 200)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            ev_schedule.generate_profile(
                schedule_start, basefreq=3, seed=seed
            )
            return Seilab(
                model_path=os.path.join(
                    "irec_seilab",
                    "fmus",
                    op_sys,
                    "IREC_SEILAB_heavy_pump_",
                ),
                EV_schedule=ev_schedule,
                simulation_days=120,
                weather="ESP_CT_Barcelona_ElPratAP1",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                ev_schedule.generate_profile(
                    schedule_start, basefreq=3, seed=seed
                )
                return Seilab(
                    model_path=os.path.join(
                        "irec_seilab",
                        "fmus",
                        op_sys,
                        "IREC_SEILAB_heavy_pump_",
                    ),
                    EV_schedule=ev_schedule,
                    **kwargs
                )  # SeilabThermal(**kwargs)
            except BaseException as e:
                print(e)
                raise Exception("Unable to build model")
    elif key == EnvNames.SEILAB_GRID_V0.value:
        ev_schedule = ElectricVehicleSchedule(30, 50, 37 / 200)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            ev_schedule.generate_profile(
                schedule_start, basefreq=3, seed=seed
            )
            return Seilab(
                model_path=os.path.join(
                    "irec_seilab",
                    "fmus",
                    op_sys,
                    "IREC_SEILAB_heavy_th_",
                ),
                EV_schedule=ev_schedule,
                simulation_days=365,
                weather="ESP_CT_Barcelona_ElPratAP1",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                ev_schedule.generate_profile(
                    schedule_start, basefreq=3, seed=seed
                )
                return Seilab(
                    model_path=os.path.join(
                        "irec_seilab",
                        "fmus",
                        op_sys,
                        "IREC_SEILAB_heavy_th_",
                    ),
                    EV_schedule=ev_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.SMARTLAB_THERMAL_V0.value:
        ev1_schedule = ElectricVehicleSchedule(30, 50, 37 / 200)
        ev2_schedule = ElectricVehicleSchedule(30, 50, 37 / 200)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            ev1_schedule.generate_profile(
                schedule_start, basefreq=3, seed=seed
            )
            ev2_schedule.generate_profile(
                schedule_start, basefreq=3, seed=seed * 100
            )
            return Smartlab(
                model_path=os.path.join(
                    "irec_smartlab",
                    "fmus",
                    op_sys,
                    "IREC_SMARTLAB_heavy_insulated_pump_",
                ),
                EV1_schedule=ev1_schedule,
                EV2_schedule=ev2_schedule,
                simulation_days=120,
                weather="ESP_CT_Barcelona_ElPratAP1",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                ev1_schedule.generate_profile(
                    schedule_start, basefreq=3, seed=seed
                )
                ev2_schedule.generate_profile(
                    schedule_start, basefreq=3, seed=seed + 100
                )
                return Smartlab(
                    model_path=os.path.join(
                        "irec_smartlab",
                        "fmus",
                        op_sys,
                        "IREC_SMARTLAB_heavy_insulated_pump_",
                    ),
                    EV1_schedule=ev1_schedule,
                    EV2_schedule=ev2_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.SMARTLAB_GRID_V0.value:
        ev1_schedule = ElectricVehicleSchedule(30, 50, 37 / 200)
        ev2_schedule = ElectricVehicleSchedule(30, 50, 37 / 200)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            ev1_schedule.generate_profile(
                schedule_start, basefreq=3, seed=seed
            )
            ev2_schedule.generate_profile(
                schedule_start, basefreq=3, seed=seed * 100
            )
            return Smartlab(
                model_path=os.path.join(
                    "irec_smartlab",
                    "fmus",
                    op_sys,
                    "IREC_SMARTLAB_heavy_insulated_",
                ),
                EV1_schedule=ev1_schedule,
                EV2_schedule=ev2_schedule,
                simulation_days=365,
                weather="ESP_CT_Barcelona_ElPratAP1",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                ev1_schedule.generate_profile(
                    schedule_start, basefreq=3, seed=seed
                )
                ev2_schedule.generate_profile(
                    schedule_start, basefreq=3, seed=seed + 100
                )
                return Smartlab(
                    model_path=os.path.join(
                        "irec_smartlab",
                        "fmus",
                        op_sys,
                        "IREC_SMARTLAB_heavy_insulated_",
                    ),
                    EV1_schedule=ev1_schedule,
                    EV2_schedule=ev2_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.DATACENTER_THERMOSTAT_V0.value:
        # cwd = os.getcwd()
        cpu_dataframe = pd.read_csv(
            os.path.join(
                dir_path,
                "schedules",
                "ScheduleFiles",
                "data_cpu.csv",  # "energym",
            )
        )
        cpu_schedule = CPUSchedule(cpu_dataframe, 10)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            cpu_schedule.generate_profile(
                schedule_start, basefreq=15, seed=seed
            )
            return DataCenter(
                model_path=os.path.join(
                    "datacenter",
                    "fmus",
                    op_sys,
                    "ZoneDataCenterHVAC_wEconomizer_thermostats_",
                ),
                cpu_schedule=cpu_schedule,
                simulation_days=365,
                weather="USA_NY_NewYork_KennedyAP3",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                cpu_schedule.generate_profile(
                    schedule_start, basefreq=15, seed=seed
                )
                return DataCenter(
                    model_path=os.path.join(
                        "datacenter",
                        "fmus",
                        op_sys,
                        "ZoneDataCenterHVAC_wEconomizer_thermostats_",
                    ),
                    cpu_schedule=cpu_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.DATACENTER_TEMP_FAN_V0.value:

        cpu_dataframe = pd.read_csv(
            os.path.join(
                dir_path, "schedules", "ScheduleFiles", "data_cpu.csv"
            )
        )
        cpu_schedule = CPUSchedule(cpu_dataframe, 10)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            cpu_schedule.generate_profile(
                schedule_start, basefreq=15, seed=seed
            )
            return DataCenter(
                model_path=os.path.join(
                    "datacenter",
                    "fmus",
                    op_sys,
                    "DataCenterHVAC_wEconomizer_Temp_Fan_",
                ),
                cpu_schedule=cpu_schedule,
                simulation_days=365,
                weather="USA_NY_NewYork_KennedyAP3",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                cpu_schedule.generate_profile(
                    schedule_start, basefreq=15, seed=seed
                )
                return DataCenter(
                    model_path=os.path.join(
                        "datacenter",
                        "fmus",
                        op_sys,
                        "DataCenterHVAC_wEconomizer_Temp_Fan_",
                    ),
                    cpu_schedule=cpu_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.OFFICES_THERMOSTAT_V0.value:
        if eval_mode:
            return Offices(
                model_path=os.path.join(
                    "offices",
                    "fmus",
                    op_sys,
                    "Offices_Thermostat_",
                ),
                simulation_days=365,
                weather="GRC_TC_Lamia1",
            )
        else:
            try:
                return Offices(
                    model_path=os.path.join(
                        "offices",
                        "fmus",
                        op_sys,
                        "Offices_Thermostat_",
                    ),
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.SILO_FAN_FCU_V0.value:
        if eval_mode:
            return Silo(
                model_path=os.path.join(
                    "silo",
                    "fmus",
                    op_sys,
                    "Silo_ahu_",
                ),
                simulation_days=365,
                weather="GRC_TC_Lamia1",
            )
        else:
            try:
                return Silo(
                    model_path=os.path.join(
                        "silo",
                        "fmus",
                        op_sys,
                        "Silo_ahu_",
                    ),
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.SEMINARCENTER_THERMOSTAT_V0.value:

        CO2_dataframe = pd.read_csv(
            os.path.join(
                dir_path, "schedules", "ScheduleFiles", "ProductionDE.csv"
            ),
            index_col=0,
        )
        CO2_schedule = EProductionSchedule(CO2_dataframe)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            CO2_schedule.generate_profile(
                schedule_start, basefreq=10, seed=seed
            )
            return Seminarcenter(
                model_path=os.path.join(
                    "seminarcenter",
                    "fmus",
                    op_sys,
                    "Seminarcenter_Thermostat_",
                ),
                CO2_schedule=CO2_schedule,
                simulation_days=151,
                weather="DNK_MJ_Horsens2",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                CO2_schedule.generate_profile(
                    schedule_start, basefreq=10, seed=seed
                )
                return Seminarcenter(
                    model_path=os.path.join(
                        "seminarcenter",
                        "fmus",
                        op_sys,
                        "Seminarcenter_Thermostat_",
                    ),
                    CO2_schedule=CO2_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.SEMINARCENTER_FULL_V0.value:

        CO2_dataframe = pd.read_csv(
            os.path.join(
                dir_path, "schedules", "ScheduleFiles", "ProductionDE.csv"
            ),
            index_col=0,
        )
        CO2_schedule = EProductionSchedule(CO2_dataframe)
        if eval_mode:
            start_day = 1
            start_month = 1
            start_year = 2019
            schedule_start = datetime.datetime(
                start_year, start_month, start_day
            )
            seed = 1
            CO2_schedule.generate_profile(
                schedule_start, basefreq=10, seed=seed
            )
            return Seminarcenter(
                model_path=os.path.join(
                    "seminarcenter",
                    "fmus",
                    op_sys,
                    "Seminarcenter_Fullcontrol_",
                ),
                CO2_schedule=CO2_schedule,
                simulation_days=151,
                weather="DNK_MJ_Horsens2",
            )
        else:
            try:
                if "start_day" in kwargs:
                    start_day = kwargs["start_day"]
                else:
                    start_day = 1
                if "start_month" in kwargs:
                    start_month = kwargs["start_month"]
                else:
                    start_month = 1
                if "start_year" in kwargs:
                    start_year = kwargs["start_year"]
                else:
                    start_year = 2019
                schedule_start = datetime.datetime(
                    start_year, start_month, start_day
                )
                seed = datetime.datetime.now().microsecond
                CO2_schedule.generate_profile(
                    schedule_start, basefreq=10, seed=seed
                )
                return Seminarcenter(
                    model_path=os.path.join(
                        "seminarcenter",
                        "fmus",
                        op_sys,
                        "Seminarcenter_Fullcontrol_",
                    ),
                    CO2_schedule=CO2_schedule,
                    **kwargs
                )
            except:
                raise Exception("Unable to build model")
    elif key == EnvNames.SIMPLE_HOUSE_RAD_V0.value:
        if eval_mode:
            return SimpleHouse(
                model_path=os.path.join(
                    "simple_house",
                    "fmus",
                    op_sys,
                    "modelica_simple_house_src_HP_u_Rad_1RC_Sun_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SimpleHouse(
                model_path=os.path.join(
                    "simple_house",
                    "fmus",
                    op_sys,
                    "modelica_simple_house_src_HP_u_Rad_1RC_Sun_",
                ),
                **kwargs
            )
    elif key == EnvNames.SIMPLE_HOUSE_SLAB_V0.value:
        if eval_mode:
            return SimpleHouse(
                model_path=os.path.join(
                    "simple_house",
                    "fmus",
                    op_sys,
                    "modelica_simple_house_src_HP_u_Slab_1RC_Sun_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SimpleHouse(
                model_path=os.path.join(
                    "simple_house",
                    "fmus",
                    op_sys,
                    "modelica_simple_house_src_HP_u_Slab_1RC_Sun_",
                ),
                **kwargs
            )
    elif key == EnvNames.SWISSHOUSE_RAD_S16_V0.value:
        if eval_mode:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Rad_1RC_Sun_S16_v0_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Rad_1RC_Sun_S16_v0_",
                ),
                **kwargs
            )
    elif key == EnvNames.SWISSHOUSE_RAD_S18_V0.value:
        if eval_mode:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Rad_1RC_Sun_S18_v0_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Rad_1RC_Sun_S18_v0_",
                ),
                **kwargs
            )
    elif key == EnvNames.SWISSHOUSE_RAD_S20_V0.value:
        if eval_mode:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Rad_1RC_Sun_S20_v0_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Rad_1RC_Sun_S20_v0_",
                ),
                **kwargs
            )
    elif key == EnvNames.SWISSHOUSE_SLAB_S16_V0.value:
        if eval_mode:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Slab_1RC_Sun_S16_v0_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Slab_1RC_Sun_S16_v0_",
                ),
                **kwargs
            )
    elif key == EnvNames.SWISSHOUSE_SLAB_S18_V0.value:
        if eval_mode:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Slab_1RC_Sun_S18_v0_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Slab_1RC_Sun_S18_v0_",
                ),
                **kwargs
            )
    elif key == EnvNames.SWISSHOUSE_SLAB_S20_V0.value:
        if eval_mode:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Slab_1RC_Sun_S20_v0_",
                ),
                weather="CH_ZH_Maur",
                simulation_days=365,
            )
        else:
            return SwissHouse(
                model_path=os.path.join(
                    "swiss_house",
                    "fmus",
                    op_sys,
                    "modelica_swisshouse_src_HP_u_Slab_1RC_Sun_S20_v0_",
                ),
                **kwargs
            )
    else:
        raise Exception("Invalid environment name.")
