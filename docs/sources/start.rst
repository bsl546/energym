.. _start:

Getting Started
*****************

Energym provides simulation environments for building control, without assuming any familiarity with the underlying simulation frameworks. The application of control strategies and their performance evaluation is made simple.

This document provides an introduction to Energym and its functionalities. For more sophisticated examples, see :ref:`examples`.


.. _my-installation:

Installation
------------

Energym can be installed in two ways:

- via a **minimal installation**, that can be used to run Energym models, benchmark controllers, but not compile new or existing models; See :ref:`install_min`.

- via a **full installation**, that requires to install all dependencies to compile new models. This installation mode should only be used by users willing to contribute to Energym models library; See :ref:`install_full`.

To ease both installation cases, three dockerfiles are provided to the users:

- the standard dockerfile (called Dockerfile) will proceed to a minimal installation within a Ubuntu 20.04 container.

- the JModelica dockerfile (called JModelica) will proceed to a full installation within a Ubuntu 18.04 container. It uses the latest freely available version of JModelica (provided in the code as a zip file), as well as Python2.7. Unfortunately, JModelica and Python2.7 are not (freely) maintained anymore, and hence this dockerfile will be deprecated in future versions, replaced by the OpenModelica one (see below).

- the Openmodelica dockerfile (called OpenModelica) will proceed to a full installation within a Ubuntu 20.04 container with Python3. The compatibility with the modelica buildings library is however still not fully guaranteed.

For more details, see :ref:`install_full`.

Setting up an Environment
--------------------------

To use Energym, it has to be imported like any other Python module using the command:

.. code-block:: python

    import energym

A simulation environment can then be created using the ``make`` command. Here we demonstrate the usage for the model :ref:`Apartments2Grid-v0 <Apartments2Grid>`.:

.. code-block:: python

    envName = "Apartments2Grid-v0"
    env = energym.make(envName)

To create a simulation environment with a different model, substitute ``envName`` with a string containing the name of one of the available models (see e.g. here :ref:`envs`).

Interacting with the Environment
---------------------------------

Once the environment has been created, control actions can be passed to it via the ``step`` method. The control actions are provided as a dictionary with pairs of input variable names and values. After performing the simulation step an observation dictionary is returned, containing output value names and their corresponding values. The inputs that have to be provided and the outputs are different for every model, their value references can be seen in their individual documentations under :ref:`buildings`. 
In code, this looks as follows:

.. code-block:: python

    inputs = {'P1_T_Thermostat_sp':[21], 'P2_T_Thermostat_sp':[21], 'P3_T_Thermostat_sp':[21], 'P4_T_Thermostat_sp':[21], 'Bd_Pw_Bat_sp':[0], 'Bd_Ch_EV1Bat_sp':[0], 'Bd_Ch_EV2Bat_sp':[0]}
    outputs = env.step(inputs)


Getting forecasts
-------------------------------

Each environment has a get_forecast() method, with which the user can retrieve meteorological and (depending on the environment) other stochastic forecasts. To get the current forecasts,

.. code-block:: python

    forecast = env.get_forecast(forecast_length=10)

is used. It outputs a dictionary with the forecasted keys over the horizon forecast_length.




Evaluating Control Performance
-------------------------------

Each environment has a :ref:`KPI <kpi_doc>` object, which keeps track of the evaluation metrics. Which evaluation metrics get tracked is determined by the ``kpi_options`` parameter for each model (see the :ref:`model documentations <model_doc>` or the :ref:`KPI documentation <kpi_doc>`). To get the current KPIs, the command

.. code-block:: python

    kpi_results = env.get_kpi()

is used. For a detailed example of the KPI use, see :ref:`here <kpi_ex>`.



Using Wrappers
-----------------------

For control, it may be useful to rescale automatically outputs and inputs, or to downsample the interactions with the simulation. This possibility is offered thanks to the implementation of wrappers
around the main Env class.  We provide an example  of iterative application of wrappers below. It leads to a rescaled, downsampled and RL-type step environment ( at the latest wrapper stage, the step method is transformed to
gives the same outputs as the  gym step method, i.e. outputs, reward, done, info = step (..).

.. code-block:: python

    import energym
    from energym.wrappers.downsample_outputs import DownsampleOutputs
    from energym.wrappers.rescale_outputs import RescaleOutputs
    from energym.wrappers.rl_wrapper import RLWrapper

    weather = "ESP_CT_Barcelona"
    env = energym.make("Apartments2Thermal-v0", weather=weather, simulation_days=300)

    downsampling_dic = ...  #define how keys are downsampled (e.g. {key1: np.mean, key2: ... }
    lower_bound =  ... #define how keys are rescaled (lower and upper bounds) (e.g. lower_bound = {key1: 0.0, ...}, upper_bound ={key1:20.0,...}
    def reward = ... #define the reward function


    env_down = DownsampleOutputs(env, steps, downsampling_dic)
    env_down_res = RescaleOutputs(env_down,lower_bound,upper_bound)
    env_down_RL = RLWrapper(env_down_res, reward)


Forecasts are automatically adapted to match the chosen rescaling and downsampling. 