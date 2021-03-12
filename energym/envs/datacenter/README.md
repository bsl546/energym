# Description of the Datacenter models

The datacenter is a two zone building with a separate HVAC system for each zone. Each HVAC sytem contains:
- an outdoor air system for air exchange with the outdoor air
- a variable volume (VAV) fan to adjust the air flow
- a direct evaporative cooler (DEC) to cool the airflow
- an indirect evaporative cooler (IEC) to cool the airflow without adding humidity
- a direct expansion cooling coil (DX CC) to cool the airflow through a heat exchanger
- a chilled water cooling coil (CW CC) to cool the airflow with chilled water

The two models of the datacenter offer different controllability and are adapted from the model described in [Reinforcement Learning Testbed for
Power-Consumption Optimization](https://arxiv.org/abs/1808.10427).

# Control

The model ``DatacenterThermostat-v0`` offers a high level control, with controllability of the zone temperature setpoints `Z01_T_Thermostat_sp` and `Z02_T_Thermostat_sp`.

The model `DatacenterTempFan-v0` admits a more low level control, where the collective temperature setpoints of the intermediate nodes of the HVAC system are set using `Z01_T_HVAC_sp` and `Z02_T_HVAC_sp`. In addition the fan flow rates are controlled with `Z01_Fl_Fan_sp` and `Z02_Fl_Fan_sp`.

For the simulation, an individual CPU loading schedule can be defined using the input `Bd_Load_CPU`. 