from enum import Enum


class EnvNames(Enum):
    """Defines the keys for the simulation environment names."""

    SMARTLAB_THERMAL_V0 = "SmartlabThermal-v0"
    SMARTLAB_GRID_V0 = "SmartlabGrid-v0"
    SEILAB_THERMAL_V0 = "SeilabThermal-v0"
    SEILAB_GRID_V0 = "SeilabGrid-v0"
    DATACENTER_THERMOSTAT_V0 = "DatacenterThermostat-v0"
    DATACENTER_TEMP_FAN_V0 = "DatacenterTempFan-v0"
    OFFICES_THERMOSTAT_V0 = "OfficesThermostat-v0"
    SILO_FAN_FCU_V0 = "SiloFanFCU-v0"
    SEMINARCENTER_THERMOSTAT_V0 = "SeminarcenterThermostat-v0"
    SEMINARCENTER_FULL_V0 = "SeminarcenterFull-v0"
    SIMPLE_HOUSE_RAD_V0 = "SimpleHouseRad-v0"
    SIMPLE_HOUSE_SLAB_V0 = "SimpleHouseSlab-v0"
    SWISSHOUSE_RAD_S18_V0 = "SwissHouseRad-v0"

    #Next names are trial versions and should not be used (will be Deprecated)
    SWISSHOUSE_RAD_S16_V0 = "SwissHouseRadS16-v0"
    SWISSHOUSE_RAD_S20_V0 = "SwissHouseRadS20-v0"
    SWISSHOUSE_SLAB_S16_V0 = "SwissHouseSlabS16-v0"
    SWISSHOUSE_SLAB_S18_V0 = "SwissHouseSlabS18-v0"
    SWISSHOUSE_SLAB_S20_V0 = "SwissHouseSlabS20-v0"