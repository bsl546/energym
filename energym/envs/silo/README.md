# Description of Silo model

The Silo building is situated at an altitude of 10 meters over sea level, and has a total surface area of 566.38m2 and a total air volume of 2208.27m3. It includes the following 13 thermal zones:
- Bathroom Ground floor
- Kitchen
- Entrance Ground floor
- Control Room
- Atrium
- Atrium
- Atrium
- Meeting Room
- Living Room P1
- Office Room 2
- Office Room 1
- Living Room P1 (Roof)
- Storage Room

# Control

In the Silo model `SiloFanFCU-v0`, some zone temperature setpoints are controllable, as well as the temperature and flow rates of the two air handling units (AHUs). The controls are named:
- Zone temperature setpoints: `Z01_T_Thermostat_sp`, `Z02_T_Thermostat_sp`, `Z03_T_Thermostat_sp`, `Z04_T_Thermostat_sp`, `Z05_T_Thermostat_sp`, `Z08_T_Thermostat_sp`, `Z09_T_Thermostat_sp`, `Z10_T_Thermostat_sp`, `Z11_T_Thermostat_sp`
- AHU temperature setpoints: `Bd_T_AHU1_sp`, `Bd_T_AHU2_sp`
- AHU air flow setpoints: `Bd_Fl_AHU1_sp`, `Bd_Fl_AHU2_sp`