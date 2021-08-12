import logging
import os

from energym.envs.env_fmu import EnvFMU
from energym.envs.utils.weather import MOS
from energym.envs.weather_names import WEATHERNAMES
import energym

logger = logging.getLogger(__name__)


class EnvModFMU(EnvFMU):
    """Base class for Modelica based FMU simulation models.

    Subclasses EnvFMU and inherits its behavior. Defines Modelica
    specific simulation details.

    Methods
    --------
    set_model_variables(variables, values)
        Sets value of model variables (Modelica).
    get_variable_data(list_vars)
        Retrieves data for a list of variables.
    """

    def __init__(
        self,
        model_path,
        start_time,
        stop_time,
        step_size,
        weather,
        params,
        init_vals,
        input_specs,
        output_specs,
        kpi_options,
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
        default_path : bool, optional
            Whether to use the default path or an absolute path in model_path and weather


        Raises
        ------
        Exception
            If the passed weather file is not contained in the list of
            available weather files
        """
        self.params = params
        if default_path:
            path = os.path.abspath(energym.__file__)
            path = os.path.abspath(os.path.join(path, "..", ".."))
            fmu_file = os.path.join(
                path,
                "simulation",
                "modelica",
                model_path + ".fmu",
            )

        else:
            fmu_file = model_path

        if weather is None:
            super().__init__(
                fmu_file,
                start_time,
                stop_time,
                step_size,
                weather,
                input_specs,
                output_specs,
                kpi_options,
                default_path,
            )
            self.look_for_weather_file()
        else:
            weather_mos = MOS()
            if default_path:
                if weather in WEATHERNAMES:
                    weather_file = os.path.join(
                        path,
                        "simulation",
                        "modelica",
                        model_path.split(os.sep)[0],
                        "wf",
                        WEATHERNAMES[weather] + ".mos",
                    )

                    weather_mos.read(
                        weather_file,
                        generate_forecasts,
                        generate_forecast_method,
                        generate_forecast_keys,
                    )
                else:
                    raise Exception("Unknown weather file")
            else:
                weather_file = weather
                weather_mos.read(
                    weather,
                    generate_forecasts,
                    generate_forecast_method,
                    generate_forecast_keys,
                )

            super().__init__(
                fmu_file,
                start_time,
                stop_time,
                step_size,
                weather_mos,
                input_specs,
                output_specs,
                kpi_options,
                default_path,
                weather_file,
            )
        self.init_vals = {key: init_vals[key] for key in self.input_keys}
        print("the initial variables are", self.init_vals)

        self.set_model_variables(list(params.keys()), list(params.values()))
        self.set_model_variables(
            list(self.init_vals.keys()), list(self.init_vals.values())
        )

    def set_model_variables(self, variables, values):
        """Sets value of model variables.

        Parameters
        ----------
        variables: str or list
            list of variables to set
        values: str or list
            list of values to set
        """
        if self.is_fmu_initialized:
            logger.warning(
                "FMU is already initialized. Values set may not be propagated in model as expected."
            )
        if isinstance(variables, str):
            self.set_model_variables([variables], [values])
        elif isinstance(variables, list):
            self.fmu.setReal([self.vrs[v] for v in variables], values)
        else:
            TypeError("variables should be list of str")

    def get_variable_data(self, list_vars):
        """Retrieves data for a list of variables.

        Parameters
        ----------
        list_vars : list
            List of variables to retrieve. Variables can be outputs of the model or internal variables.

        Returns
        -------
        dict
            Dictionary with values for the variables.
        """

        # get the values
        out_values = self.fmu.getReal([self.vrs[key] for key in list_vars])
        res = [(self.time, out_values)]
        return self.post_process(list_vars, res)

    def get_output(self):
        out = self.fmu.getReal([self.vrs[key] for key in self.output_keys])
        res = [(self.time, out)]
        output = self.post_process(self.output_keys, res, arrays=False)
        return output

    def reset(self):
        super().reset()
        self.set_model_variables(list(self.params.keys()), list(self.params.values()))
        self.set_model_variables(
            list(self.init_vals.keys()), list(self.init_vals.values())
        )
