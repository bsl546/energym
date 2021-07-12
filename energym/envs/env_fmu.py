import os
import math
import shutil
import time
import collections
from pathlib import Path
import logging
import uuid

import numpy as np
from fmpy.fmi1 import FMU1Slave, FMU1Model
from fmpy.fmi2 import FMU2Slave, FMU2Model
from fmpy import read_model_description, extract

from energym.envs.env import Env
from energym.envs.utils.weather import EPW, MOS
from energym.envs.utils.kpi import KPI
from energym.spaces.dict import Dict
from energym.spaces.discrete import Discrete
from energym.spaces.box import Box

logger = logging.getLogger(__name__)


class EnvFMU(Env):
    """The FMU base class for Energym.

    It encapsulates an environment whose simulation is performed in an FMU.
    The methods step(), reset() and close() from Env are implemented here.

    Attributes
    ----------
    fmu_file : str
        Full path to the FMU file
    model_description : fmpy ModelDescription object
        Encapsulated description of the model extracted from the FMU using
        FMPy inspection methods
    fmi_version : str
        Version number of FMI, inspected inside the FMU. Should be '1.0'
        or '2.0'
    step_size : int or double
        Simulation stepsize in seconds. Int for EnergyPlus, double for Modelica
    weather : str
        Indicates the used weather profile
    is_fmu_initialized : bool
        Flags the FMU initialization process
    vrs : dict
        Contains the variable names and their references
    fmi_type : str
        The simulation type as speified by the FMU, either 'cosim' or 'modex'
    start_time : int
        Start of simulation time in seconds
    stop_time : int
        End of simulation time in seconds
    kpis : KPI object
        To track the KPI relevant metrics
    input_space : dict
        Contains controllable input variables
    output_space : dict
        Contains output variables
    observation_history : list
        Collects all observations of one simulation
    unzipdir : str
        Directory for extracting the FMU
    fmu : FMU1Slave or FMU2Slave or FMU1Model or FMU2Model
        Simulation object
    time : int or double
        Current simulation time (int for EnergyPlus, double for Modelica)


    Methods
    -------
    initialize()
        Initializes simulation object.
    __build_input_space(input_specs)
        Collects the inputs from the simulation object.
    __build_output_space(output_specs)
        Collects the outputs from the simulation object.
    __initialize_fmu()
        Initializes the FMU after instantiation.
    get_inputs_names()
        Retrieves list of inputs from model description.
    get_outputs_names()
        Retrieves list of outputs from model description.
    get_date()
        Gets the current simulation time.
    step(inputs=None)
        Advances the simulation one timestep.
    print_kpis()
        Prints the KPIs.
    get_kpi(start_ind=0, end_ind=-1)
        Retrieves the KPIs.
    get_cumulative_kpi(phrase, kpi_type, out_type)
        Retrieves the cumulative KPIs over multiple variables.
    sample_random_action()
        Samples random actions from the action space.
    get_forecast(forecast_length = 24, **kwargs)
        Generates a weather forecast of a given length.
    look_for_weather_file(name = None)
        Finds a weather file in the FMU.
    post_process(list_rel_out, res, arrays=False)
        Post-process output of FMPY.
    reset()
        Resets the simulation.
    close()
        Terminates the FMU and removes leftover folders.

    """

    def __init__(
        self,
        model_path,
        start_time,
        stop_time,
        step_size,
        weather=None,
        input_specs=None,
        output_specs=None,
        kpi_options=None,
        default_path=True,
        weather_file_path=None,
    ):
        """
        Parameters
        ----------
        model_path: str
            Path to the fmu model file, relative inside the simulation folder
        start_time: int
            Begin of the simulation time in seconds in relation to the
            beginning of the year
        stop_time: int
            End of the simulation time in seconds in relation to the
            beginning of the year
        step_size: double
            Step size in second. May be chosen freely for some models (modelica),
            or needs to be identical to model step size in other cases (EnergyPlus)
        weather : EPW or MOS, optional
            Specifies the used weather file, by default None
        input_specs : dict, optional
            Contains the model inputs, by default None
        output_specs : dict, optional
            Contains the model outputs, by default None
        kpi_options : dict, optional
            Dict to specify the tracked KPIs, by default None
        default_path : bool
            Whether to use the deault path or an absolute path in model_path


        Raises
        ------
        ValueError
            If the FMU supprts neither co-simulation nor model exchange
        """
        super().__init__()
        if default_path:
            self.fmu_file = self.energym_path / "simulation" / model_path
        else:
            self.fmu_file = model_path
        self.model_description = read_model_description(self.fmu_file)
        self.step_size = step_size
        self.weather = weather
        self.weather_file_path = weather_file_path
        self.is_fmu_initialized = False

        # Extract variables references
        self.vrs = {}
        for variable in self.model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference

        # detect fmi_version
        self.fmi_version = self.model_description.fmiVersion

        # detect FMI type
        if self.model_description.coSimulation is not None:
            self.fmi_type = "cosim"
        elif self.model_description.modelExchange is not None:
            self.fmi_type = "modex"
        else:
            raise ValueError("the type of FMU could not be identified")

        # extract the FMU
        self.start_time = start_time
        self.stop_time = stop_time

        self.input_specs = input_specs
        self.output_specs = output_specs

        # Fix inputs and outputs keys
        if output_specs is not None:
            self.output_keys = sorted(
                [
                    p.name
                    for p in self.model_description.modelVariables
                    if p.name in list(output_specs.keys())
                ]
            )
            self.__build_output_space(output_specs)
        else:
            self.output_keys = sorted(
                [
                    p.name
                    for p in self.model_description.modelVariables
                    if p.causality == "output"
                ]
            )

        if input_specs is not None:
            self.input_keys = sorted(
                [
                    p.name
                    for p in self.model_description.modelVariables
                    if p.name in list(input_specs.keys())
                ]
            )
            self.__build_input_space(input_specs)
        else:
            self.input_keys = sorted(
                [
                    p.name
                    for p in self.model_description.modelVariables
                    if p.causality == "input"
                ]
            )

        self.kpis = KPI(kpi_options)

        # # initialize FMU and spaces
        self.initialize()

    def __build_input_space(self, input_specs):
        """Collects the inputs from the simulation object.

        The inputs have to be contained in input_specs  but
        not every key of the two needs to be an input to the specific model.

        Parameters
        ----------
        input_specs : dict
            Contains possible control inputs from the model.


        """
        input_array = self.get_inputs_names()
        input_space_list = []

        for act_name in input_array:
            if act_name in input_specs:
                act_specs = input_specs[act_name]
                if act_specs["type"] == "scalar":
                    input_space_list += [
                        (
                            act_name,
                            Box(
                                low=act_specs["lower_bound"],
                                high=act_specs["upper_bound"],
                                shape=[1],
                                dtype=np.float32,
                            ),
                        )
                    ]
                elif act_specs["type"] == "discrete":
                    input_space_list += [(act_name, Discrete(act_specs["size"]))]
                else:
                    raise TypeError("Wrong type in INPUT_SPECS.")

            else:
                raise ValueError("Undefined Input {}".format(act_name))

        self.input_space = Dict(spaces=input_space_list)

    def __build_output_space(self, output_specs):
        """Collects the outputs from the simulation object.

        The outputs have to be contained in output_specs, but not every
        key needs to be an output to the specific model.

        Parameters
        ----------
        output_specs : dict
            Contains possible outputs from the model.
        """
        output_array = self.get_outputs_names()

        output_space_list = []
        for obs_name in output_array:
            obs_specs = output_specs[obs_name]
            if obs_specs["type"] == "scalar":
                output_space_list += [
                    (
                        obs_name,
                        Box(
                            low=obs_specs["lower_bound"],
                            high=obs_specs["upper_bound"],
                            shape=[1],
                            dtype=np.float32,
                        ),
                    )
                ]
            elif obs_specs["type"] == "discrete":
                output_space_list += [(obs_name, Discrete(obs_specs["size"]))]
        self.output_space = Dict(spaces=output_space_list)
        self.observation_history = []

    def __initialize_fmu(self):
        """Initializes the FMU after instantiation."""
        if self.fmi_version == "1.0":
            self.fmu.initialize(tStart=self.start_time, stopTime=self.stop_time)
        elif self.fmi_version == "2.0":
            self.fmu.enterInitializationMode()
            self.fmu.exitInitializationMode()
        self.is_fmu_initialized = True

    def initialize(self):
        """Initializes simulation object.

        Instantiates FMPy FMUSalve1 or FMUSlave2 object based on FMI
        version detected.
        """
        init_time = str(time.time())[0:10]
        random_id = str(uuid.uuid4().fields[-1])[:7]
        fmu_path = os.path.join(self.runs_path, init_time + "_" + random_id)
        os.mkdir(fmu_path)
        self.unzipdir = extract(self.fmu_file, unzipdir=fmu_path)
        weather_folder = Path(self.unzipdir) / "resources"
        possible_weather_files = list(weather_folder.rglob("*.mos")) + list(
            weather_folder.rglob("*.epw")
        )
        weather_default_file_path = weather_folder / possible_weather_files[0]
        try:
            os.remove(weather_default_file_path)
            shutil.copy(self.weather_file_path, weather_default_file_path)
        except BaseException as e:
            logging.error(e)
            logging.error("Problem with the weather file handling")
        # initialize
        instance_name = "instance" + init_time

        # model identifier
        if self.fmi_type == "modex":
            model_id = self.model_description.modelExchange.modelIdentifier
        else:
            model_id = self.model_description.coSimulation.modelIdentifier

        kwargs = dict(
            guid=self.model_description.guid,
            unzipDirectory=self.unzipdir,
            modelIdentifier=model_id,
            instanceName=instance_name,
        )

        if self.fmi_version == "1.0":
            if self.fmi_type == "cosim":
                self.fmu = FMU1Slave(**kwargs)
            else:
                self.fmu = FMU1Model(**kwargs)
        elif self.fmi_version == "2.0":
            if self.fmi_type == "cosim":
                self.fmu = FMU2Slave(**kwargs)
            else:
                self.fmu = FMU2Model(**kwargs)

        self.fmu.instantiate(loggingOn=True)
        if self.fmi_version == "2.0":
            self.fmu.setupExperiment(startTime=self.start_time, stopTime=self.stop_time)

        # Initialize time and the last_output values
        self.time = self.start_time

    def get_inputs_names(self):
        """Retrieves list of inputs from model description.

        Returns
        -------
        input_keys : list of str
            List with input names.
        """

        return self.input_keys

    def get_outputs_names(self):
        """Retrieves list of outputs from model description.

        Returns
        -------
        output_keys : list of str
            Variable names that specify outputs.
        """

        return self.output_keys  # res

    def get_date(self):
        """Gets the current simulation time.

        Returns
        -------
        int
            Minutes of the current simulation time
        int
            Hours of the current simulation time
        int
            Day of the current simulation time
        int
            Month of the current simulation time
        """

        time_tuple = (2013, 1, 1, 0, 0, 0, 1, 1, 0)
        base_time = time.mktime(time_tuple)
        date = time.localtime(base_time + self.time)
        return date[4], date[3], date[2], date[1]

    def step(self, inputs=None):
        """Advances the simulation one timestep.

        Applies input for current step, simulate the system in FMU and retrieves outputs.

        Parameters
        ----------
        inputs: dict
            Inputs for the system. Keys are input names, values are iterables of input values.
            If not defined, assumes no inputs required.

        Returns
        ----------
        outputs: dict
            Outputs for the system.
        """
        if inputs is None:
            inputs = {}
        # Initializes FMU is not already
        if not self.is_fmu_initialized:
            self.__initialize_fmu()
        # Inputs is a dictionary of arrays
        res = []

        # simulation loop
        if bool(inputs):
            inp_keys = sorted(list(inputs.keys()))
            n_steps = len(inputs[inp_keys[0]])
            non_inp_keys = set(self.input_keys) - set(list(inputs))
        else:
            n_steps = 1
            inp_keys = []
            non_inp_keys = self.input_keys
        for p in range(n_steps):
            key_list = []
            input_list = []
            for key in inp_keys:
                key_list.append(self.vrs[key])
                input_list.append(inputs[key][p])
            for key in non_inp_keys:
                key_list.append(self.vrs[key])
                input_list.append(self.input_specs[key]["default"])
            self.fmu.setReal(
                key_list,
                input_list,
            )

            # perform one step
            self.fmu.doStep(
                currentCommunicationPoint=self.time,
                communicationStepSize=self.step_size,
            )

            # get the values
            out_values = self.fmu.getReal([self.vrs[key] for key in self.output_keys])

            # advance the time
            self.time += self.step_size

            # append the results
            res.append((self.time, out_values))

        output = self.post_process(self.output_keys, res, arrays=False)

        self.kpis.add_observation(output)
        return output

    def print_kpis(self):
        """Prints the KPIs."""
        kpi_summary = self.get_kpi()
        for key in kpi_summary:
            print(
                "####################################################################"
            )
            kpi_name = kpi_summary[key]["name"]
            kpi_type = kpi_summary[key]["type"]
            kpi_val = kpi_summary[key]["kpi"]
            print(
                "Variable name: {}, kpi type: {}, kpi value: {}".format(
                    kpi_name, kpi_type, kpi_val
                )
            )

    def get_kpi(self, start_ind=0, end_ind=-1):
        """Retrieves the KPIs.

        For implementation details see the KPI class.

        Parameters
        ----------
        start_ind : int, optional
            Index from where the KPI computation starts, by default 0
        end_ind: int, optional
            Index where the KPI computation ends, by default -1

        Returns
        -------
        kpi_summary : dict
            Dict containing all the tracked variables and their KPIs.
        """
        return self.kpis.get_kpi(start_ind, end_ind)

    def get_cumulative_kpi(self, names, kpi_type, out_type):
        """Retrieves the cumulative KPIs over multiple variables.

        For implementation details see the KPI class.

        Parameters
        ----------
        names : list or str
            List of variable names or common string to filter the variables.
        kpi_type : str
            One of the 4 KPI types to filter the variables.
        out_type : str
            Cumulative KPI type ("avg" or "sum").

        Returns
        -------
        float or int
            The computed KPI.
        """
        return self.kpis.get_cumulative_kpi(names, kpi_type, out_type)

    def sample_random_action(self):
        """Samples random actions from the action space.

        Returns
        -------
        dict
            Inputs with random values, within a specified range
        """
        action = self.input_space.sample()
        return dict(list(action.items()))

    def get_forecast(self, forecast_length=24):
        """Generates a weather forecast of a given length.

        Parameters
        ----------
        forecast_length : int, optional
            Number of timesteps that will be forecasted, by default 24

        Returns
        -------
        forecast : dict
            Forecasted values for default keys or ones specified in kwargs
        """
        time_resolution = self.step_size / 60
        hourly_steps = int(60 / time_resolution)
        tot_length = math.ceil(forecast_length / hourly_steps) + 2
        start_index = 0
        forecast = {}

        if isinstance(self.weather, EPW):
            minute, hour, day, month = self.get_date()
            start_index = int(minute / time_resolution)
            forecast = self.weather.get_forecast(hour, day, month, tot_length)

        elif isinstance(self.weather, MOS):
            res = self.time % 3600
            start_index = int(res / self.step_size)
            forecast = self.weather.get_forecast(self.time - res, forecast_length)
        forecast = self._interpolate_forecast(forecast, hourly_steps)
        for key in forecast:
            forecast[key] = forecast[key][start_index : forecast_length + start_index]
        return forecast

    def _interpolate_forecast(self, forecast, hourly_steps):
        for key in forecast:
            mod_list = forecast[key]
            new_list = []
            for i in range(len(mod_list) - 1):
                for j in range(hourly_steps):
                    weight = j / hourly_steps
                    new_list.append(
                        (1 - weight) * mod_list[i] + weight * mod_list[i + 1]
                    )
            new_list.append(mod_list[len(mod_list) - 1])
            forecast[key] = new_list
        return forecast

    def look_for_weather_file(
        self,
        name=None,
        generate_forecasts=True,
        generate_forecast_method="perfect",
        generate_forecast_keys=None,
    ):
        """Finds a weather file in the FMU.

        Parameters
        ----------
        name : str
            Name of weather file

        Raises
        ------
        Exception
            If no weather file/more than one weather file is found or the file has a wrong type
        """
        weather_folder = Path(self.unzipdir) / "resources"
        if name is None:
            possible_weather_files = list(weather_folder.rglob("*.mos")) + list(
                weather_folder.rglob("*.epw")
            )
        else:
            possible_weather_files = list(weather_folder.rglob(name))
        if len(possible_weather_files) == 0:
            raise Exception("No weather file found in FMU")
        elif len(possible_weather_files) > 1:
            raise Exception(
                "Found more than one weather file: {}. specify a name to select one.".format(
                    possible_weather_files
                )
            )
        else:
            wf = weather_folder / possible_weather_files[0]
            if wf.suffix == ".mos":
                self.weather = MOS()
                self.weather.read(
                    wf,
                    generate_forecasts,
                    generate_forecast_method,
                    generate_forecast_keys,
                )
            elif wf.suffix == ".epw":
                self.weather = EPW()
                self.weather.read(
                    wf,
                    generate_forecasts,
                    generate_forecast_method,
                    generate_forecast_keys,
                )
            else:
                raise Exception(
                    "File {} cannot be interpreted as a weather file".format(wf)
                )

    def post_process(self, list_rel_out, res, arrays=False):
        """Post-process output of FMPY.

        Parameters
        ----------
        list_rel_out : list of str
            Output labels
        res : list
            Output of doStep FMPy method
        arrays : bool, optional
            If True, array output in processed structure, default is False

        Returns
        -------
        dic_res: collections.OrderedDict
            Dictionary with values of output for each key
        """
        N = len(res)
        dic_res = collections.OrderedDict()
        position = {e: i for i, e in enumerate(list_rel_out)}

        # Store time
        if arrays:
            dic_res["time"] = []

            for key in list_rel_out:
                dic_res[key] = []

        for p in range(N):
            for key in list_rel_out:
                if arrays:
                    dic_res[key] += [res[p][1][position[key]]]
                else:
                    dic_res[key] = res[p][1][position[key]]
            if arrays:
                dic_res["time"] += [res[p][0]]
            else:
                dic_res["time"] = res[p][0]
        if arrays:
            for key in dic_res:
                dic_res[key] = np.asarray(dic_res[key]).flatten()
        return dic_res

    def reset(self):
        """Resets the simulation."""
        self.close()
        self.kpis.reset()
        self.initialize()

    def close(self, save=True):
        """Terminates the FMU and removes leftover folders."""
        instance_name = self.fmu.instanceName
        self.fmu.terminate()
        self.fmu.freeInstance()
        self.is_fmu_initialized = False
        try:
            shutil.rmtree(self.unzipdir)
        except PermissionError as e:
            logger.error(f"Folder could not be removed. {e}")
        cwd = os.getcwd()
        wd_sub_list = os.listdir(cwd)
        if save:
            for directory in wd_sub_list:
                if instance_name in directory:
                    try:
                        shutil.move(
                            os.path.join(cwd, directory),
                            os.path.join(self.runs_path, directory),
                        )
                    except PermissionError as e:
                        logger.error(f"Folder could not be moved. {e}")
        else:
            for directory in wd_sub_list:
                if instance_name in directory:
                    try:
                        shutil.rmtree(
                            os.path.join(cwd, directory),
                        )
                    except PermissionError as e:
                        logger.error(f"Folder could not be removed. {e}")
