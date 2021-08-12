from enum import Enum


class EnvNames(Enum):
    """Defines the keys for the simulation environment names."""

    APARTMENTS2_THERMAL_V0 = "Apartments2Thermal-v0"
    APARTMENTS2_GRID_V0 = "Apartments2Grid-v0"
    APARTMENTS_THERMAL_V0 = "ApartmentsThermal-v0"
    APARTMENTS_GRID_V0 = "ApartmentsGrid-v0"
    OFFICES_THERMOSTAT_V0 = "OfficesThermostat-v0"
    MIXEDUSE_FAN_FCU_V0 = "MixedUseFanFCU-v0"
    SEMINARCENTER_THERMOSTAT_V0 = "SeminarcenterThermostat-v0"
    SEMINARCENTER_FULL_V0 = "SeminarcenterFull-v0"
    SIMPLE_HOUSE_RAD_V0 = "SimpleHouseRad-v0"
    SIMPLE_HOUSE_SLAB_V0 = "SimpleHouseSlab-v0"
    SIMPLE_HOUSE_RSLA_V0 = "SimpleHouseRSla-v0"
    SWISSHOUSE_RSLA_W2W_V0 = "SwissHouseRSlaW2W-v0"
    SWISSHOUSE_RSLA_A2W_V0 = "SwissHouseRSlaA2W-v0"
    SWISSHOUSE_RSLA_TANK_V0 = "SwissHouseRSlaTank-v0"
    SWISSHOUSE_RSLA_TANK_DHW_V0 = "SwissHouseRSlaTankDhw-v0"