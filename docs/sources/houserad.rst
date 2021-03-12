.. _SimpleHouserad:


SimpleHouseRad
----------------


The simple house is a one-zone residential buildings located in Zurich Canton, Switzerland


Building and thermal zones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The entire house is modeled with a single thermal zone.



Thermal systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A Heat pump with Carnot HX connected to a simple room model with radiator. A schematic picture of the equipment is given in the following image:


.. image:: images/HP_u_Rad_1_RC_Sun.png


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

For more detail, please check the documentation :ref:`simplehouse_doc` or the source code in :py:class:`energym.envs.simple_house.simple_house.SimpleHouse`.


.. exec::
    import json
    from energym.envs.simple_house.simple_house import INPUTS_SPECS
    table = ".. csv-table:: \n    :header: Variable Name, Type, Lower Bound, Upper Bound, # States\n\n"
    for var in INPUTS_SPECS:
        table = table + "    " + var + ", " + "" + INPUTS_SPECS[var]["type"] + ", "
        if INPUTS_SPECS[var]["type"] == "scalar":
            table = table + str(INPUTS_SPECS[var]["lower_bound"]) + ", " + str(INPUTS_SPECS[var]["upper_bound"]) + ", "
        else:
            table = table + ", , " + str(INPUTS_SPECS[var]["size"])
        table = table + "\n"
    print(table)
        



Simulation outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. exec::
    import json
    from energym.envs.simple_house.simple_house import OUTPUTS_SPECS_RAD
    table = ".. csv-table:: \n    :header: Variable Name, Type, Lower Bound, Upper Bound, # States\n\n"
    for var in OUTPUTS_SPECS_RAD:
        table = table + "    " + var + ", " + "" + OUTPUTS_SPECS_RAD[var]["type"] + ", "
        if OUTPUTS_SPECS_RAD[var]["type"] == "scalar":
            table = table + str(OUTPUTS_SPECS_RAD[var]["lower_bound"]) + ", " + str(OUTPUTS_SPECS_RAD[var]["upper_bound"]) + ", "
        else:
            table = table + ", , " + str(OUTPUTS_SPECS_RAD[var]["size"])
        table = table + "\n"
    print(table)


Evaluation scenario
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The evaluation scenario for the `SimpleHouseRad-v0` model consists of a control from January to April with the objective of minimizing the power demand, while keeping the zone temperatures between 19 and 24°C.
For this goal, the tracked KPIs are the average power demand, and the average temperature deviation and total temperature violations with respect to the interval [19, 24].

Notebook example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1
   :caption:  Here is a notebook example:

   notebooks/SimpleHouseSlab