.. _apiref:

API Reference
***************

.. contents:: 
    :local:
    :depth: 3

Main Classes
##############

The Env class
-----------------

.. autoclass:: energym.envs.env.Env
    :members:


The EnvFmu class
---------------------

.. autoclass:: energym.envs.env_fmu.EnvFMU
    :members:


The EnvEPlusFMU class
---------------------------

.. autoclass:: energym.envs.env_fmu_eplus.EnvEPlusFMU
    :members:

.. _model_doc:

Model Classes
################

.. _seminarcenter_doc:

The Seminarcenter environment
-----------------------------------------

.. autoclass:: energym.envs.seminarcenter.seminarcenter.Seminarcenter

.. _apartments_doc:

The Apartments environment
------------------------------------

.. autoclass:: energym.envs.apartments.apartments.Apartments

.. _apartments2_doc:

The Apartments2 environment
-----------------------------------------

.. autoclass:: energym.envs.apartments2.apartments2.Apartments2

.. _offices_doc:

The Offices environment
--------------------------------

.. autoclass:: energym.envs.offices.offices.Offices

.. _mixeduse_doc:

The MixedUse environment
--------------------------------

.. autoclass:: energym.envs.mixeduse.mixeduse.MixedUse

.. _simplehouse_doc:

The SimpleHouse environment
---------------------------------------

.. autoclass:: energym.envs.simple_house.simple_house.SimpleHouse

.. _swisshouse_doc:

The SwissHouse environment
-------------------------------------

.. autoclass:: energym.envs.swiss_house.swiss_house.SwissHouse


Wrappers
##############

The abstract Wrapper class
---------------------------

.. autoclass:: energym.envs.env.Wrapper
    :members:

The abstract OutputsWrapper class
----------------------------------

.. autoclass:: energym.envs.env.OutputsWrapper
    :members:

The abstract StepWrapper class
----------------------------------

.. autoclass:: energym.envs.env.StepWrapper
    :members:

The abstract InputsWrapper class
----------------------------------

.. autoclass:: energym.envs.env.InputsWrapper
    :members:

OutputsWrapper
-----------------

.. autoclass:: energym.wrappers.rescale_outputs.RescaleOutputs
    :members:

.. autoclass:: energym.wrappers.transform_outputs.TransformOutputs
    :members:

.. autoclass:: energym.wrappers.filter_outputs.FilterOutputs
    :members:

StepWrapper
------------

.. autoclass:: energym.wrappers.downsample_outputs.DownsampleOutputs
    :members:

.. autoclass:: energym.wrappers.rl_wrapper.RLWrapper
    :members:

InputsWrapper
--------------

.. autoclass:: energym.wrappers.clip_inputs.ClipInputs
    :members:

.. autoclass:: energym.wrappers.rescale_inputs.RescaleInputs
    :members:


Utils and Main Functions
##########################

The make method
-----------------

.. autofunction:: energym.factory.make

.. _kpi_doc:

The KPI class
-----------------------

.. autoclass:: energym.envs.utils.kpi.KPI
    :members:

The weather classes
---------------------------

.. autoclass:: energym.envs.utils.weather.Weather
    :members:

.. autoclass:: energym.envs.utils.weather.EPW
    :members:

.. autoclass:: energym.envs.utils.weather.MOS
    :members: