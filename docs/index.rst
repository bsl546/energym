.. energym documentation master file, created by
   sphinx-quickstart on Wed Feb 19 15:59:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree:: 
   :hidden:
   :maxdepth: 2
   
   sources/base

   sources/install_min

   sources/start

   sources/Examples

   sources/install_full

   sources/add_model

   sources/apiref




Energym
================================


Energym is an open source building simulation library designed for the control community to test  climate control and energy mangement strategies on buildings in a systematic and reproducible way. Energym includes a number of building models that are calibrated on site data and defines standard metrics, quantifying the objective to be reached and allowing a standardized comparison between different controllers and publications.
 
The  library offers an intuitive interface to a variety of building models, similar to the one popularized by the `Gym <https://gym.openai.com/>`_ used in the robotic control community. Energym relies on the `functional mockup interface (FMI) <https://fmi-standard.org/>`_ standard in order to support models generated in multiple modelling languages easily. It incorporates models developed in  `Modelica <https://www.modelica.org/>`_ and `EnergyPlus <https://energyplus.net/>`_  as well as specific classes for simulating weather forecasts and appliances consumption figures.
 
Energym has to date 14 models integrated and  offers the possibility to benchmark controllers on buildings models that are representative of real-world HVAC systems. They cover different buildings typologies (institutional building, office building, etc.) and configuration of the HVAC where control can be performed at different levels (control of energy generation, control of final demand through setpoints, etc.). 

New models and new control capabilities are under development und will be added to the library in due course.

.. It runs on top of Energyplus and JModellica. Both are available for free and can be installed automatically using conda forge; see :ref:`my-installation`.


The library is compatible both for windows 10 and linux os and provides precompiled fmu files for both operating systems. 
Two docker files (one for running current models, one for compiling new models) that download dockerhub pre-built images are also at user disposal to speed up use and testing.


.. raw:: html

    <style> .red {color:#DC143C; font-weight:bold; font-size:16px} </style>
    <style> .gre {color:#32cd32; font-weight:bold; font-size:16px} </style>
    <style> .yel {color:#E6E6FA; font-weight:bold; font-size:16px} </style>


.. role:: red

.. role:: gre

.. role:: yel




Features
--------

- Works directly on Windows and Linux (pre-compiled buildings .fmu files)
- Works with E+ and Modelica
- Works with Python 3.*


.. _envs:

Available environments
----------------------

Following environments are available. Click on the buildings hyperlink to get complete descriptions 
of the buildings, their inputs and outputs.

   

+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| Technical systems/                                                  |Thermostat | Heatpump   | AHU        | Battery  |  EV      |  PV        |Prg|
| Buildings                                                           |           |            |            |          |          |            |   |
+=====================================================================+===========+============+============+==========+==========+============+===+
| :ref:`ApartmentsThermal-v0 <ApartmentsThermal>`                     |:gre:`con` |:gre:`con`  |:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`ApartmentsGrid-v0 <ApartmentsGrid>`                           |:gre:`con` |:yel:`uncon`|:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`Apartments2Thermal-v0 <Apartments2Thermal>`                   |:gre:`con` |:gre:`con`  |:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`Apartments2Grid-v0 <Apartments2Grid>`                         |:gre:`con` |:yel:`uncon`|:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`OfficesThermostat-v0 <Offices>`                               |:gre:`con` |:red:`abs`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`MixedUseFanFCU-v0 <MixedUse>`                                 |:gre:`con` |:red:`abs`  |:gre:`con`  |:red:`abs`|:red:`abs`|:red:`abs`  | E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SeminarcenterThermostat-v0 <SeminarcenterThermostat>`         |:gre:`con` |:yel:`uncon`|:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SeminarcenterFull-v0 <SeminarcenterFull>`                     |:gre:`con` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SimpleHouseRad-v0 <SimpleHouserad>`                           |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SimpleHouseRSla-v0 <SimpleHouseslab>`                         |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SwissHouseRSlaW2W-v0 <SwissHousesla>`                         |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SwissHouseRSlaA2W-v0 <SwissHousesla>`                         |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SwissHouseRSlaTank-v0 <SwissHouseslatank>`                    |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SwissHouseRSlaTankDhw-v0 <SwissHouseslatank>`                 |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+

:gre:`con` : present and controllable, :yel:`uncon` : present but uncontrollable, :red:`abs` : absent.


..
   .. toctree::
   :maxdepth: 1
   :caption: Buildings description:
   
   sources/smartt

   sources/smartg
   
   sources/seit
   
   sources/seig

   sources/offices

   sources/mixeduse

   sources/seminart

   sources/seminarf

   sources/houserad

   sources/houseslab

   sources/swiss

   sources/swiss2

Example
----------

The usage of Energym is straight forward, as in this simplified code example, assuming the implementation of a ``get_input()`` function made by the user:

.. code-block:: python

   import energym

   envName = "Apartments2Grid-v0"
   nsteps = 10
   env = energym.make(envName, simulation_days=100)
   obs = env.get_output()
   for _ in range(nsteps):
      inputs = get_input(obs)
      obs = env.step(inputs)
   env.close()

For an introduction to Energym see :ref:`start` and for more in depth control examples see :ref:`Examples`.


Philosophy
--------------

Energym  has been designed such that you are entirely free in your controller strategy and design. 

In particular, if you use Model Predictive Control or Reinforcement Learning strategies, a set of weather files at different locations close to the real location is provided to carry out system identification/ RL training.

When a controller/model has been trained, it can be finally evaluated on the predefined period of time under the predefined meto condition and KPIs.

Furthermore, models can be launched in parallels, making Energym models also usable for flexibility control strategies at multi-building level.





Contribute
----------

Users are encouraged to upload new environments that present an interest for building or energy system control.

To do so, follow the full installation steps described  in :ref:`install_full`.

To create a new model, please  follow the steps described in :ref:`add_model`. Then contact the authors (see Support) if you want your model to be incorporated in Energym.

Cite
-------

If you use our library for your work, please cite our paper: 

Scharnhorst, P.; Schubnel, B.; Fernández Bandera, C.; Salom, J.; Taddeo, P.; Boegli, M.; Gorecki, T.; Stauffer, Y.; Peppas, A.; Politi, C. Energym: A Building Model Library for Controller Benchmarking. Appl. Sci. 2021, 11, 3518. https://doi.org/10.3390/app11083518 



Support
-------

If you are having issues, please let us know and open an issue on github. We are happy to let Energym grow and help you in a reasonable amount of time.


License
-------

The project  is licensed under the BSD license. 

Thanks
-------

Part of this work has been carried out under European Project Sabina. Research institutes and partners involved are `CSEM <https://www.csem.ch/Home>`_, `IREC <https://www.irec.cat/>`_, `UNAV <https://www.unav.edu/en/home>`_, `NTUA <https://www.ntua.gr/en/>`_ and `INSERO <https://inserohorsens.dk/>`_.

.. figure:: sources/images/logo_csem.svg
   :height: 40
   :target: https://www.csem.ch/Home

.. figure:: sources/images/IREC-Logo.png
   :height: 60
   :target: https://www.irec.cat/

.. figure:: sources/images/UNAV.svg
   :height: 60
   :target: https://www.unav.edu/en/home

.. figure:: sources/images/ntualogo.png
   :height: 80
   :target: https://www.ntua.gr/en/

.. figure:: sources/images/inserohorsens_wide.png
   :height: 40
   :target: https://inserohorsens.dk/

..
   .. image:: sources/images/csem_irec_unav.PNG






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
