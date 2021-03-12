# Description of the Offices model

The Offices building is situated at an altitude of 4 meters over sea level, and has a total surface area of 643.73m2 and a total air volume of 2504.54m3. It includes the following 25 conditioned rooms:
- 3 Storage Rooms.
- 4 Seminar Rooms.
- 2 Central Rooms (Lobbies).
- 3 Corridors.
- 1 Staircase
- 4 WC (Bathrooms).
- 1 Kitchen.
- 5 Office Spaces.
- 1 Meeting Room.
- 1 HVAC air handling equipment room.

# Control

The Offices model `OfficesThermostat-v0` offers a high level control over temperature setpoints for certain rooms. These setpoints are named:
- `Z01_T_Thermostat_sp`, `Z02_T_Thermostat_sp`, `Z03_T_Thermostat_sp`, `Z04_T_Thermostat_sp`, `Z05_T_Thermostat_sp`, `Z06_T_Thermostat_sp`, `Z07_T_Thermostat_sp`, `Z15_T_Thermostat_sp`, `Z16_T_Thermostat_sp`, `Z17_T_Thermostat_sp`, `Z18_T_Thermostat_sp`, `Z19_T_Thermostat_sp`, `Z20_T_Thermostat_sp`, `Z25_T_Thermostat_sp`

The rooms that are not directly controlled are:
- the corridors, the Bathrooms, the staircase, the kitchen, the HVAC room and one of the storage rooms.