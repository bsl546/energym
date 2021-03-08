import os

import energym
from energym.envs.env_fmu import EnvFMU
from energym.envs.utils.weather import EPW
from energym.envs.weather_names import WEATHERNAMES


class EnvEPlusFMU(EnvFMU):
    """Base class for EnergyPlus based FMU simulation models.

    Subclasses EnvFMU and inherits its behavior. Defines EnergyPlus
    specific simulation details.
    """

    def __init__(
        self,
        model_path,
        start_time,
        stop_time,
        step_size,
        # ep_version,
        weather,
        input_specs,
        output_specs,
        kpi_options,
        default_path=True,
    ):
        """
        Parameters
        ----------
        model_path : str
            Specifies the path to the FMU
        start_time : int
            Begin of the simulation time in seconds in relation to the
            beginning of the year
        stop_time : int
            End of the simulation time in seconds in relation to the
            beginning of the year
        step_size : float
            Length of a simulation timestep in seconds
        weather : str
            Specifies the used weather file
        input_specs : dict
            Contains the inputs of the model
        output_specs : dict
            Contains the outputs of the model
        kpi_options : dict
            Dict to specify the tracked KPIs.
        default_path : bool
            Whether to use the default path or an absolute path in model_path and weather


        Raises
        ------
        Exception
            If the passed weather file is not contained in the list of
            available weather files
        """
        weather_epw = EPW()
        if default_path:
            if weather in WEATHERNAMES:

                path = os.path.abspath(energym.__file__)
                path = os.path.abspath(os.path.join(path, "..", ".."))

                fmu_file = os.path.join(
                    path,
                    "simulation",
                    "energyplus",
                    model_path + WEATHERNAMES[weather] + ".fmu",
                )
                weather_file = os.path.join(
                    path,
                    "simulation",
                    "energyplus",
                    model_path.split(os.sep)[0],
                    "wf",
                    WEATHERNAMES[weather] + ".epw",
                )

                weather_epw.read(weather_file)
            else:
                raise Exception("Unknown weather file")
        else:
            weather_epw.read(weather)
            fmu_file = model_path

        super().__init__(
            fmu_file,
            start_time,
            stop_time,
            step_size,
            weather_epw,
            input_specs,
            output_specs,
            kpi_options,
            default_path,
        )

    def initialize(self):

        """Initializes simulation object.

        Instantiates FMPy FMUSalve1 or FMUSlave2 object based on FMI
        version detected. For E+, by default, an empty stepp is made at the beginning
        and default step parameters are done.
        """
        super().initialize()
        self._last_output = {}
        _ = self.step({})

    def step(self, inputs={}):
        output = super().step(inputs)
        self._last_output = output
        return output

    def get_output(self):
        return self._last_output
