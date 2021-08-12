.. _SwissHouseslatank:


SwissHouseRSlaTank
--------------------

The SwissHouse building is a one-zone residential building located in Zurich Canton, Switzerland. 


Building and thermal zones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The entire house is modeled with a single thermal zone. Its envelop is a simple RC model with R, C parameters
fitted to a real swiss Minergie house (low energy consumption building standard).


Thermal systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Heat is provided by a water to water heat pump, connected to a tank. The tanks serves as a supply to the hydronic underfloor heating.
In the version SwissHouseRSlaTankDhw-v0, a hot water tank for hot water consumption is added and connected to the pump as well.
The building has no cooling system.

The picture below displays the SwissHouseRSlaTank systems.

.. image:: images/SwissHouse_HP_u_Tank_u_RSla_1RC_Sun.png
    :width: 600
    :align: center

The picture below displays the SwissHouseRSlaTankDhw systems.

.. image:: images/SwissHouse_HP_u_Tank_u_DHW_u_RSla_1RC_Sun.png
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

Tank control
""""""""""""""""""
The normalized flow from the tank to the room is controllable.

Valve control
""""""""""""""""""
The valve opening (water flow to the hot water tank) is controllable. This is only the case for the moder with hot water tank.



Simulation inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For more detail, please check the documentation :ref:`swisshouse_doc` or the source code in :py:class:`energym.envs.swiss_house.swiss_house.SwissHouse`.


.. exec::
    import json
    from energym.envs.swiss_house.swiss_house import INPUTS_SPECS
    table = ".. csv-table:: \n    :header: Variable Name, Type, Lower Bound, Upper Bound, # States, Description\n\n"
    for var in INPUTS_SPECS:
        if var!="u":
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
The evaluation scenario for the `SwissHouseRSlaTank-v0` model consists of a control from January to April with the objective of minimizing the power demand, while keeping the zone temperatures between 19 and 24°C.
For this goal, the tracked KPIs are the average power demand, and the average temperature deviation and total temperature violations with respect to the interval [19, 24]. For the model with hot water consumption, 
there is no prescribed consumption flow fraction rate yet, and the user can choose/ implement typical hot water consumption patterns. 

Notebook example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1
   :caption:  Here is a notebook example:

   notebooks/SwissHouseRSlaTank