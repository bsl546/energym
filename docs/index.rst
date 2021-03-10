.. energym documentation master file, created by
   sphinx-quickstart on Wed Feb 19 15:59:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree:: 
   :hidden:
   :maxdepth: 2
   
   sources/base

   sources/start

   sources/install_min

   sources/install_full

   sources/add_model

   sources/Examples

   sources/apiref


.. figure:: sources/images/Energym2.PNG
   :height: 320

Energym
================================


Energym is a calibrated open source building simulation library designed for the control community to test climate control and energy mangement strategies on buildings in a systematic and reproducible way. Energym includes a number of building models that are calibrated on site data and defines standard metrics, quantifying the objective to be reached and allowing a standardized comparison between different controllers and publications.
 
The  library offers an intuitive interface to a variety of building models, similar to the one popularized by the `Gym <https://gym.openai.com/>`_ used in the robotic control community. Energym relies on the `functional mockup interface (FMI) <https://fmi-standard.org/>`_ standard in order to support models generated in multiple modelling languages easily. It currently includes seven models developed in `Modelica <https://www.modelica.org/>`_ and `EnergyPlus <https://energyplus.net/>`_  as well as specific classes for simulating weather forecasts and appliances consumption figures.
 
With the models already incorporated, Energym offers the possibility to benchmark controllers on buildings models that are representative of real-world HVAC systems. They cover different buildings typologies (institutional building, office building, etc.) and configuration of the HVAC where control can be performed at different levels (control of energy generation, control of final demand through setpoints, etc.). In summary, the models already incorporated are representative of cases that can be encountered in real-world control deployment.


.. It runs on top of Energyplus and JModellica. Both are available for free and can be installed automatically using conda forge; see :ref:`my-installation`.


The library is compatible both for windows 10 and linux os and provides precompiled fmu files for both operating systems. 
A docker container file is also provided for users wanting to build the library within a container.


.. raw:: html

    <style> .red {color:#aa0060; font-weight:bold; font-size:16px} </style>
    <style> .gre {color:#32cd32; font-weight:bold; font-size:16px} </style>
    <style> .yel {color:#f9ee44; font-weight:bold; font-size:16px} </style>


.. role:: red

.. role:: gre

.. role:: yel




Features
--------

- Works directly (pre-compiled buildings .fmu files)
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
| :ref:`SmartlabThermal-v0 <SmartlabThermal>`                         |:gre:`con` |:gre:`con`  |:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SmartlabGrid-v0 <SmartlabGrid>`                               |:gre:`con` |:yel:`uncon`|:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`ApartmentsThermal-v0 <ApartmentsThermal>`                     |:gre:`con` |:gre:`con`  |:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`ApartmentsGrid-v0 <ApartmentsGrid>`                           |:gre:`con` |:yel:`uncon`|:red:`abs`  |:gre:`con`|:gre:`con`|:yel:`uncon`| E+|
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
| :ref:`SimpleHouseSlab-v0 <SimpleHouseslab>`                         |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
+---------------------------------------------------------------------+-----------+------------+------------+----------+----------+------------+---+
| :ref:`SwissHouseRad-v0 <SwissHouserad>`                             |:red:`abs` |:gre:`con`  |:red:`abs`  |:red:`abs`|:red:`abs`|:yel:`uncon`|Mod|
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


Example
----------

The usage of Energym is straight forward, as in this simplified code example, assuming the implementation of a ``get_input()`` function:

.. code-block:: python

   import energym

   envName = "SmartlabGrid-v0"
   nsteps = 10
   env = energym.make(envName, simulation_days=100)
   obs = env.get_output()
   for _ in range(nsteps):
      inputs = get_input(obs)
      obs = env.step(inputs)
   env.close()

For an introduction to Energym see :ref:`start` and for more in depth control examples see :ref:`Examples`.


Contribute
----------

Users are encouraged to upload any new environment that present an interest for building or energy system control.

To do so, follow the full installation steps described  in :ref:`install_full`.

To create a new model, please  follow the steps described in :ref:`add_model`. Then contact the authors (see Support) if you want your model to be incorporated in Energym.

Cite
-------

If you use our library for your publication, please cite our paper. 



Support
-------

If you are having issues, please let us know. We are happy to let Energym grow and help you in a reasonable amount of time.
Plese contact the maintainers <psh@csem.ch> and <bsl@csem.ch>.

License
-------

The project except all files in "dependencies" is licensed under the BSD license. For dependencies licenses, please refer to the dependencies folder.


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
