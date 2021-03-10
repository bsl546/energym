import math


class SimpleController(object):
    """Rule-based controller for thermostat setpoint control.

    Supports the models SeminarcenterThermostat-v0
    and OfficesThermostat-v0.

    Attributes
    ----------
    controls : list of str
        List of control inputs.
    observations : list of str
        List of zone temperature observations
    tol1 : float
        First threshold for deviation from the goal temperature.
    tol2 : float
        Second threshold for deviation from the goal temperature.
    nighttime_setback : bool
        Whether to use a nighttime setback.
    nighttime_start : int
        Hour to start the nighttime setback.
    nighttime_end : int
        Hour to end the nighttime setback.
    nighttime_temp : float
        Goal temperature during nighttime setback

    Methods
    -------
    get_control(obs, temp_sp, hour)
        Computes the control actions.
    """

    def __init__(
        self,
        control_list,
        lower_tol,
        upper_tol,
        nighttime_setback=False,
        nighttime_start=17,
        nighttime_end=6,
        nighttime_temp=18,
    ):
        """
        Parameters
        ----------
        control_list : list of str
            List containing all inputs
        lower_tol : float
            First threshold for deviation from the goal temperature.
        upper_tol : float
            Second threshold for deviation from the goal temperature.
        nighttime_setback : bool, optional
            Whether to use a nighttime setback, by default False.
        nighttime_start : int, optional
            Hour to start the nighttime setback, by default 17
        nighttime_end : int, optional
            Hour to end the nighttime setback, by default 6
        nighttime_temp : int, optional
            Goal temperature during nighttime setback, by default 18

        Raises
        ------
        TypeError
            If wrong input types are detected.
        """

        for control in control_list:
            if "T_Thermostat_sp" not in control:

                raise TypeError(
                    "Only thermostat setpoints are supported by this controller!"
                )
        self.controls = control_list

        self.observations = [control[0:5] for control in self.controls]
        self.tol1 = lower_tol
        self.tol2 = upper_tol
        self.nighttime_setback = nighttime_setback
        self.nighttime_start = nighttime_start
        self.nighttime_end = nighttime_end
        self.nighttime_temp = nighttime_temp

    def get_control(self, obs, temp_sp, hour=0):
        """Computes the control actions.

        Parameters
        ----------
        obs : dict
            Dict containing the temperature observations.
        temp_sp : float
            Goal temperature for the next timestep.
        hour : int
            Current hour in the simulation time.

        Returns
        -------
        controls : dict
            Dict containing the control inputs.
        """
        controls = {}
        if self.nighttime_setback:
            if hour < self.nighttime_end or hour > self.nighttime_start:
                for control in self.controls:
                    controls[control] = [self.nighttime_temp]
            else:
                for control in self.controls:
                    controls[control] = [temp_sp]
        else:
            for control in self.controls:
                controls[control] = [temp_sp]
        for measurement in self.observations:
            control_name = measurement + "_Thermostat_sp"
            observation = obs[measurement]
            control_temp = controls[control_name][0]
            if (
                observation - control_temp < self.tol1
                and control_temp - observation < self.tol1
            ):
                control_temp = control_temp
            elif self.tol1 < observation - control_temp < self.tol2:
                control_temp = control_temp - 0.1
            elif observation - control_temp > self.tol2:
                control_temp = control_temp - 0.5
            elif self.tol1 < control_temp - observation < self.tol2:
                control_temp = control_temp + 0.1
            elif control_temp - observation > self.tol2:
                control_temp = control_temp + 0.5
            controls[control_name][0] = control_temp

        return controls


class LabController(object):
    """Rule-based controller for temperature control.

    Supports the models ApartmentsThermal-v0, ApartmentsGrid-v0,
    Apartments2Thermal-v0 and Apartments2Grid-v0.

    Attributes
    ----------
    thermostat_controls : list of str
        List of inputs for thermostat control.
    HP_temp_controls : list of str
        List of inputs for heat pump temperature control.
    HP_onoff_controls : list of str
        List of inputs for heat pump on/off control.
    observations : list of str
        List of zone temperature observations
    tol1 : float
        First threshold for deviation from the goal temperature.
    tol2 : float
        Second threshold for deviation from the goal temperature.
    nighttime_setback : bool
        Whether to use a nighttime setback.
    nighttime_start : int
        Hour to start the nighttime setback.
    nighttime_end : int
        Hour to end the nighttime setback.
    nighttime_temp : float
        Goal temperature during nighttime setback

    Methods
    -------
    get_control(obs, temp_sp, hour)
        Computes the control actions.
    """

    def __init__(
        self,
        control_list,
        lower_tol,
        upper_tol,
        nighttime_setback=False,
        nighttime_start=17,
        nighttime_end=6,
        nighttime_temp=18,
    ):
        """
        Parameters
        ----------
        control_list : list of str
            List containing all inputs
        lower_tol : float
            First threshold for deviation from the goal temperature.
        upper_tol : float
            Second threshold for deviation from the goal temperature.
        nighttime_setback : bool, optional
            Whether to use a nighttime setback, by default False.
        nighttime_start : int, optional
            Hour to start the nighttime setback, by default 17
        nighttime_end : int, optional
            Hour to end the nighttime setback, by default 6
        nighttime_temp : int, optional
            Goal temperature during nighttime setback, by default 18
        """
        self.thermostat_controls = []
        self.HP_temp_controls = []
        self.HP_onoff_controls = []
        for control in control_list:
            if "T_Thermostat_sp" in control:
                self.thermostat_controls.append(control)
            elif "T_HP_sp" in control:
                self.HP_temp_controls.append(control)
            elif "onoff_HP_sp" in control:
                self.HP_onoff_controls.append(control)
        self.observations = ["Z0" + str(i + 1) + "_T" for i in range(8)]
        self.tol1 = lower_tol
        self.tol2 = upper_tol
        self.nighttime_setback = nighttime_setback
        self.nighttime_start = nighttime_start
        self.nighttime_end = nighttime_end
        self.nighttime_temp = nighttime_temp

    def get_control(self, obs, temp_sp, hour):
        """Computes the control actions.

        Parameters
        ----------
        obs : dict
            Dict containing the temperature observations.
        temp_sp : float
            Goal temperature for the next timestep.
        hour : int
            Current hour in the simulation time.

        Returns
        -------
        controls : dict
            Dict containing the control inputs.
        """
        controls = {}
        ctrl = "P{}_T_Thermostat_sp"
        if self.nighttime_setback:
            if hour < self.nighttime_end or hour > self.nighttime_start:
                for control in self.thermostat_controls:
                    controls[control] = [self.nighttime_temp]
            else:
                for control in self.thermostat_controls:
                    controls[control] = [temp_sp]
        else:
            for control in self.thermostat_controls:
                controls[control] = [temp_sp]
        for control in self.HP_temp_controls:
            controls[control] = [50]
        for control in self.HP_onoff_controls:
            obs_name = control + "_out"
            controls[control] = [obs[obs_name]]
        for measurement in self.observations:
            number = math.ceil(int(measurement[2]) / 2)
            control_name = ctrl.format(number)
            observation = obs[measurement]
            control_temp = controls[control_name][0]
            if (
                observation - control_temp < self.tol1
                and control_temp - observation < self.tol1
            ):
                control_temp = control_temp
            elif self.tol1 < observation - control_temp < self.tol2:
                control_temp = control_temp - 0.5
            elif self.tol2 < observation - control_temp < 2 * self.tol2:
                control_temp = control_temp - 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [0]
            elif observation - control_temp > self.tol2:
                control_temp = control_temp - 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [0]
                for control in self.HP_temp_controls:
                    controls[control] = [45]
            elif self.tol1 < control_temp - observation < self.tol2:
                control_temp = control_temp + 0.5
            elif self.tol2 < control_temp - observation < 2 * self.tol2:
                control_temp = control_temp + 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [1]
            elif control_temp - observation > 2 * self.tol2:
                control_temp = control_temp + 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [1]
                for control in self.HP_temp_controls:
                    controls[control] = [55]
            controls[control_name][0] = control_temp
        return controls


class SeminarcenterFullController(object):
    """Rule-based controller for temperature control.

    Supports the model SeminarcenterFull-v0.

    Attributes
    ----------
    thermostat_controls : list of str
        List of inputs for thermostat control.
    HP_temp_controls : list of str
        List of inputs for heat pump temperature control.
    HP_onoff_controls : list of str
        List of inputs for heat pump on/off control.
    HVAC_controls : list of str
        List of inputs for HVAC equipment temperature control.
    hotwater_controls : list of str
        List of inputs for hot water temperature control.
    observations : list of str
        List of zone temperature observations
    tol1 : float
        First threshold for deviation from the goal temperature.
    tol2 : float
        Second threshold for deviation from the goal temperature.
    nighttime_setback : bool
        Whether to use a nighttime setback.
    nighttime_start : int
        Hour to start the nighttime setback.
    nighttime_end : int
        Hour to end the nighttime setback.
    nighttime_temp : float
        Goal temperature during nighttime setback

    Methods
    -------
    get_control(obs, temp_sp, hour)
        Computes the control actions.
    """

    def __init__(
        self,
        control_list,
        lower_tol,
        upper_tol,
        nighttime_setback=False,
        nighttime_start=17,
        nighttime_end=6,
        nighttime_temp=18,
    ):
        """
        Parameters
        ----------
        control_list : list of str
            List containing all inputs
        lower_tol : float
            First threshold for deviation from the goal temperature.
        upper_tol : float
            Second threshold for deviation from the goal temperature.
        nighttime_setback : bool, optional
            Whether to use a nighttime setback, by default False.
        nighttime_start : int, optional
            Hour to start the nighttime setback, by default 17
        nighttime_end : int, optional
            Hour to end the nighttime setback, by default 6
        nighttime_temp : int, optional
            Goal temperature during nighttime setback, by default 18
        """
        self.thermostat_controls = []
        self.HP_temp_controls = []
        self.HP_onoff_controls = []
        self.HVAC_controls = []
        self.hotwater_controls = []
        self.boiler_controls = []
        self.AHU_controls = []
        self.other_temp_controls = []
        for control in control_list:
            if "T_Thermostat_sp" in control:
                self.thermostat_controls.append(control)
            elif "T_HP" in control:
                self.HP_temp_controls.append(control)
            elif "onoff_HP" in control:
                self.HP_onoff_controls.append(control)
            elif "T_HVAC" in control:
                self.HVAC_controls.append(control)
            elif "T_Hotwater" in control:
                self.hotwater_controls.append(control)
            elif "T_Boiler" in control:
                self.boiler_controls.append(control)
            elif "T_AHU" in control:
                self.AHU_controls.append(control)
            elif "T_buffer" in control or "T_mixer" in control:
                self.other_temp_controls.append(control)
        self.observations = [control[:5] for control in self.thermostat_controls]
        self.tol1 = lower_tol
        self.tol2 = upper_tol
        self.nighttime_setback = nighttime_setback
        self.nighttime_start = nighttime_start
        self.nighttime_end = nighttime_end
        self.nighttime_temp = nighttime_temp

    def get_control(self, obs, temp_sp, hour):
        """Computes the control actions.

        Parameters
        ----------
        obs : dict
            Dict containing the temperature observations.
        temp_sp : float
            Goal temperature for the next timestep.
        hour : int
            Current hour in the simulation time.

        Returns
        -------
        controls : dict
            Dict containing the control inputs.
        """
        controls = {}
        ctrl = "{}_Thermostat_sp"
        if self.nighttime_setback:
            if hour < self.nighttime_end or hour > self.nighttime_start:
                for control in self.thermostat_controls:
                    controls[control] = [self.nighttime_temp]
                for control in self.HVAC_controls:
                    controls[control] = [self.nighttime_temp]
            else:
                for control in self.thermostat_controls:
                    controls[control] = [temp_sp]
                for control in self.HVAC_controls:
                    controls[control] = [temp_sp]
        else:
            for control in self.thermostat_controls:
                controls[control] = [temp_sp]
        for control in self.HP_temp_controls:
            controls[control] = [50]
        for control in self.hotwater_controls:
            controls[control] = [50]
        for control in self.boiler_controls:
            controls[control] = [60]
        for control in self.AHU_controls:
            controls[control] = [25]
        for control in self.other_temp_controls:
            controls[control] = [40]

        for control in self.HP_onoff_controls:
            controls[control] = [0]  # obs[obs_name]
        for measurement in self.observations:
            control_name = ctrl.format(measurement)
            observation = obs[measurement]
            control_temp = controls[control_name][0]
            if (
                observation - control_temp < self.tol1
                and control_temp - observation < self.tol1
            ):
                control_temp = control_temp
            elif self.tol1 < observation - control_temp < self.tol2:
                control_temp = control_temp - 0.5
            elif self.tol2 < observation - control_temp < 2 * self.tol2:
                control_temp = control_temp - 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [0]
                for control in self.boiler_controls:
                    controls[control] = [50]
                for control in self.other_temp_controls:
                    controls[control] = [35]
            elif observation - control_temp > self.tol2:
                control_temp = control_temp - 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [0]
                for control in self.HP_temp_controls:
                    controls[control] = [45]
                for control in self.hotwater_controls:
                    controls[control] = [45]
                for control in self.boiler_controls:
                    controls[control] = [45]
                for control in self.other_temp_controls:
                    controls[control] = [30]
                for control in self.AHU_controls:
                    controls[control] = [20]
            elif self.tol1 < control_temp - observation < self.tol2:
                control_temp = control_temp + 0.5
            elif self.tol2 < control_temp - observation < 2 * self.tol2:
                control_temp = control_temp + 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [1]
                for control in self.boiler_controls:
                    controls[control] = [65]
                for control in self.other_temp_controls:
                    controls[control] = [45]
            elif control_temp - observation > 2 * self.tol2:
                control_temp = control_temp + 0.5
                for control in self.HP_onoff_controls:
                    controls[control] = [1]
                for control in self.HP_temp_controls:
                    controls[control] = [55]
                for control in self.hotwater_controls:
                    controls[control] = [55]
                for control in self.boiler_controls:
                    controls[control] = [70]
                for control in self.other_temp_controls:
                    controls[control] = [50]
                for control in self.AHU_controls:
                    controls[control] = [33]
            controls[control_name][0] = control_temp
        return controls


class MixedUseController(object):
    """Rule-based controller for temperature control.

    Supports the model MixedUseFanFCU-v0.

    Attributes
    ----------
    AHUfan_controls : list of str
        List of inputs for AHU fan flow rate control.
    AHUT_controls : list of str
        List of inputs for AHU temperature control.
    thermostat_controls : list of str
        List of inputs for thermostat control.
    observations : list of str
        List of zone temperature observations
    tol1 : float
        First threshold for deviation from the goal temperature.
    tol2 : float
        Second threshold for deviation from the goal temperature.
    nighttime_setback : bool
        Whether to use a nighttime setback.
    nighttime_start : int
        Hour to start the nighttime setback.
    nighttime_end : int
        Hour to end the nighttime setback.
    nighttime_temp : float
        Goal temperature during nighttime setback

    Methods
    -------
    get_control(obs, temp_sp, hour)
        Computes the control actions.
    """

    def __init__(
        self,
        control_list,
        lower_tol,
        upper_tol,
        nighttime_setback=False,
        nighttime_start=17,
        nighttime_end=6,
        nighttime_temp=18,
    ):
        """
        Parameters
        ----------
        control_list : list of str
            List containing all inputs
        lower_tol : float
            First threshold for deviation from the goal temperature.
        upper_tol : float
            Second threshold for deviation from the goal temperature.
        nighttime_setback : bool, optional
            Whether to use a nighttime setback, by default False.
        nighttime_start : int, optional
            Hour to start the nighttime setback, by default 17
        nighttime_end : int, optional
            Hour to end the nighttime setback, by default 6
        nighttime_temp : int, optional
            Goal temperature during nighttime setback, by default 18
        """
        self.AHUfan_controls = []
        self.AHUT_controls = []
        self.thermostat_controls = []
        for control in control_list:
            if "T_AHU" in control:
                self.AHUT_controls.append(control)
            elif "Fl_AHU" in control:
                self.AHUfan_controls.append(control)
            elif "T_Thermostat" in control:
                self.thermostat_controls.append(control)
        self.observations = [control[:5] for control in self.thermostat_controls]
        self.tol1 = lower_tol
        self.tol2 = upper_tol
        self.nighttime_setback = nighttime_setback
        self.nighttime_start = nighttime_start
        self.nighttime_end = nighttime_end
        self.nighttime_temp = nighttime_temp

    def get_control(self, obs, temp_sp, hour):
        """Computes the control actions.

        Parameters
        ----------
        obs : dict
            Dict containing the temperature observations.
        temp_sp : float
            Goal temperature for the next timestep.
        hour : int
            Current hour in the simulation time.

        Returns
        -------
        controls : dict
            Dict containing the control inputs.
        """
        controls = {}
        ctrl = "{}_Thermostat_sp"
        ahu = "Bd_T_{}_sp"
        fan = "Bd_Fl_{}_sp"
        if self.nighttime_setback:
            if hour < self.nighttime_end or hour > self.nighttime_start:
                control_temp = self.nighttime_temp
                for control in self.thermostat_controls:
                    controls[control] = [self.nighttime_temp]
            else:
                control_temp = temp_sp
                for control in self.thermostat_controls:
                    controls[control] = [temp_sp]
        else:
            control_temp = temp_sp
            for control in self.thermostat_controls:
                controls[control] = [temp_sp]
        for control in self.AHUfan_controls:
            controls[control] = [0]
        for control in self.AHUT_controls:
            controls[control] = [temp_sp]
        for measurement in self.observations:
            observation = obs[measurement]
            control_name = ctrl.format(measurement)
            if "Z05" in measurement:
                AHU_name = "AHU1"
                Fl_max = 10
            else:
                AHU_name = "AHU2"
                Fl_max = 1
            AHU_control = ahu.format(AHU_name)
            fan_name = fan.format(AHU_name)
            if self.tol1 < observation - control_temp < self.tol2:
                controls[control_name] = [control_temp - 1]
                controls[fan_name] = [math.ceil(Fl_max / 2)]
            elif self.tol1 < control_temp - observation < self.tol2:
                controls[control_name] = [control_temp + 1]
                controls[fan_name] = [math.ceil(Fl_max / 2)]
            elif observation - control_temp > self.tol2:
                controls[control_name] = [control_temp - 1.5]
                controls[fan_name] = [Fl_max]
                controls[AHU_control] = [control_temp - 2]
            elif control_temp - observation > self.tol2:
                controls[control_name] = [control_temp + 1.5]
                controls[fan_name] = [Fl_max]
                controls[AHU_control] = [control_temp + 2]
        return controls
