.. _SwissHousesla:


SwissHouseRSla
----------------

The SwissHouse building is a one-zone residential building located in Zurich Canton, Switzerland. 


Building and thermal zones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The entire house is modeled with a single thermal zone. Its envelop is a simple RC model with R, C parameters
fitted to a real swiss Minergie house (low energy consumption building standard).



Thermal systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Two  heat pump versions are implemented: SwissHouseRSlaW2W-v0 and SwissHouseRSlaA2W-v0.
SwissHouseRSlaW2W-v0 has a water to water heat pump, and SwissHouseRSlaA2W-v0 a air to water heat pump. Both emit heat to the zone via  hydronic underfloor heating.
The building has no cooling system.

The picture below displays the Air-to-Water systems.

.. image:: images/SwissHouse_HP_u_RSla_1RC_Sun_A2W.png
    :width: 600
    :align: center

The picture below displays the Water-to-Water systems.

.. image:: images/SwissHouse_HP_u_RSla_1RC_Sun_W2W.png
    :width: 600
    :align: center


Electrical systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The site incorporates a photovoltaic installation.  



Controllable components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


HP control
""""""""""""""""""
The heat pump normalized power is controllable.




Simulation inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For more detail, please check the documentation :ref:`swisshouse_doc` or the source code in :py:class:`energym.envs.swiss_house.swiss_house.SwissHouse`.


.. exec::
    import json
    from energym.envs.swiss_house.swiss_house import INPUTS_SPECS
    table = ".. csv-table:: \n    :header: Variable Name, Type, Lower Bound, Upper Bound, # States, Description\n\n"
    for var in INPUTS_SPECS:
        if var=="u":
            table = table + "    " + var + ", " + "" + INPUTS_SPECS[var]["type"] + ", "
            if INPUTS_SPECS[var]["type"] == "scalar":
                table = table + str(INPUTS_SPECS[var]["lower_bound"]) + ", " + str(INPUTS_SPECS[var]["upper_bound"]) + ", "
            else:
                table = table + ", , " + str(INPUTS_SPECS[var]["size"])
            table = table + ", " + str(INPUTS_SPECS[var]["description"])
            table = table + "\n"
    print(table)
        



Simulation outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. exec::
    import json
    from energym.envs.swiss_house.swiss_house import OUTPUTS_SPECS_RSLA
    table = ".. csv-table:: \n    :header: Variable Name, Type, Lower Bound, Upper Bound, # States, Description\n\n"
    for var in OUTPUTS_SPECS_RSLA:
        table = table + "    " + var + ", " + "" + OUTPUTS_SPECS_RSLA[var]["type"] + ", "
        if OUTPUTS_SPECS_RSLA[var]["type"] == "scalar":
            table = table + str(OUTPUTS_SPECS_RSLA[var]["lower_bound"]) + ", " + str(OUTPUTS_SPECS_RSLA[var]["upper_bound"]) + ", "
        else:
            table = table + ", , " + str(OUTPUTS_SPECS_RSLA[var]["size"])
        table = table + ", " + str(OUTPUTS_SPECS_RSLA[var]["description"])
        table = table + "\n"
    print(table)


Weather files
^^^^^^^^^^^^^^^^^^^^^^^^^^

The available weather files for this model have the following specifiers:

- ``CH_ZH_Maur`` (Evaluation file)
- ``CH_BS_Basel`` (Default)
- ``CH_TI_Bellinzona``
- ``CH_GR_Davos``
- ``CH_GE_Geneva``
- ``CH_VD_Lausanne``



Evaluation scenario
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The evaluation scenario for the `SwissHouseRSlaW2W-v0` model consists of a control from January to April with the objective of minimizing the power demand, while keeping the zone temperatures between 19 and 24°C.
For this goal, the tracked KPIs are the average power demand, and the average temperature deviation and total temperature violations with respect to the interval [19, 24].

Notebook example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1
   :caption:  Here is a notebook example:

   notebooks/SwissHouseRSla