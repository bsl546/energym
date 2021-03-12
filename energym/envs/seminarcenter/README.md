# Description of the Seminarcenter models

The Seminarcenter model is a one-story building situated at an altitude of 248 meters over sea level, with a total surface area of 1278.94m2 and a total air volume of 3764.95m3. It includes the following 22 conditioned rooms:
- 1 Large seminar room.
- 9 Small seminar rooms.
- 3 Storage rooms.
- 5 Cloakrooms.
- 1 Staffroom.
- 2 Bathrooms.
- 1 HVAC air handling equipment room.

And 5 additional unconditioned areas:
- 5 Roof-to-ceiling space above Cloakrooms.

For the Seminarcenter building, two models are available. The ``SeminarcenterThermostat-v0`` model gives a more high-level control, whereas the `SeminarcenterFull-v0` model offers a lower-level control.

# Control

The following elements can be controlled for ``SeminarcenterThermostat-v0``:
- 22 room temperature setpoints: ``Z02_T_Thermostat_sp``, ``Z03_T_Thermostat_sp``, ``Z04_T_Thermostat_sp``, ``Z05_T_Thermostat_sp``, ``Z06_T_Thermostat_sp``, ``Z07_T_Thermostat_sp``, ``Z08_T_Thermostat_sp``, ``Z09_T_Thermostat_sp``, ``Z10_T_Thermostat_sp``, ``Z11_T_Thermostat_sp``, ``Z12_T_Thermostat_sp``, ``Z13_T_Thermostat_sp``, ``Z14_T_Thermostat_sp``, ``Z15_T_Thermostat_sp``, ``Z16_T_Thermostat_sp``, ``Z17_T_Thermostat_sp``, ``Z18_T_Thermostat_sp``, ``Z19_T_Thermostat_sp``, ``Z20_T_Thermostat_sp``, ``Z21_T_Thermostat_sp``, ``Z22_T_Thermostat_sp``, ``Z24_T_Thermostat_sp`` 

Additional controls for `SeminarcenterFull-v0` are:
- 4 heat pump on/off setpoints: ``Bd_onoff_HP1_sp``, ``Bd_onoff_HP2_sp``, ``Bd_onoff_HP3_sp``, ``Bd_onoff_HP4_sp``
- 4 heat pump temperature setpoints: ``Bd_T_HP1_sp``, ``Bd_T_HP2_sp``, ``Bd_T_HP3_sp``, ``Bd_T_HP4_sp``
- 1 HVAC temperature setpoint: ``Bd_T_HVAC_sp``
- 1 hot water temperature setpoint: ``Bd_T_Hotwater_sp``