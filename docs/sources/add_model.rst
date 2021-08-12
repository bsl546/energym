.. _add_model:

Contributing
********************

To contribute, you must first follow the steps given in :ref:`install_full`.

Add your model
--------------------------

Depending on the type of model (Modelica/Energyplus), create a new folder in simulation/energyplus or simulation/modelica with the name of your model.
The folder must have following structure:

* fmus: where fmus will be stored. Let this directory  empty at the beginning.
* wf: weather files to be used for training and benchmarking evaluation (.epw or .mos)
* src: put here your source files (.idf or .mo)

You may want to add additional files for Modelica models. This is allowed and users are encouraged to check existing models and imitate their structure.



Compile your model
--------------------------


Energyplus
^^^^^^^^^^^^^^^^^^

We provide in the directory scripts a Python script *create_eplus_env.py*. Edit this file putting your Energyplus path and the EnergyplusToFMU path. You may also 
edit the pythoncom variable depending on your platform.

Then, in a command line, type::

    python create_eplus_env.py -folder_name <folder_name> -src <model_name>


You may want to provide a weather file with the option -wf. By default, you must have at least a weather wile called weather.epw in the weather folder.

If the compilation is successful, models are added to the fmus folder of your model.



Modelica
^^^^^^^^^^^^^^^^^^

We provide in the directory scripts a Python script *create_mo_env_jmod.py*. You may need to update the file user_config.py to point to your Modelica building library/ IBPSA building library folder.

Then, in a command line, type::

    python create_mo_env_jmod.py -folder_name <folder_name> -src <model_name>

If the compilation is successful, models are added to the fmus folder of your model.



Test your model
--------------------------

In principle, testing and documentation updates will be done by our Team to ensure that your model is working properly within our framework.

However, you can already propose a pre-implemented Energym version by:

    - adding your model to the factory method

    - adding a python script for your environment in energym.envs

    - adding your model name and weather file names in weather_names.py and env_names.py


Then, tests can be done installing Energym (python setup.py install energym) and adding a test for the model in the tests folder. Note that Energym requires python>=3.6.