.. _install_min:

Minimal Installation
********************

The minimal installation should be preferred by all users who do not contribute directly to Energym by adding new building models.

Installation steps are explained below for Linux and Windows 10.


Windows 10
--------------------------

Before starting, you must have a running version of Python>=3.6. Check `here <https://www.python.org/downloads/>`_.

1. Download Energyplus 9.4 for Windows from this  `link <https://energyplus.net/downloads>`_ and install it.

2. Edit windows environment variables, add Energyplus to your path follwing the steps:

    - Search "edit environment variables" in the taskbar, open the purposed link, click on Environment Variables.

    .. image:: images/env_var_windows1.PNG

    - Click on "Path" and then Edit as displayed below.
    
    .. image:: images/env_var_windows2.PNG

    - Add your Energyplus installation path.

    .. image:: images/env_var_windows3.PNG


3. Install Energym. You can directly install Energym from pypi with pip::

    pip install energym


   Or you can install Energym from its source gitlab repository, with git::

    git clone <energym adress>
    cd <energym main folder>
    python setup.py install --verbose




Linux (Ubuntu)
--------------------------

Before starting, you must have a running version of Python>=3.6. Check `here <https://www.python.org/downloads/>`_.

1. Make sure you have gcc, g++, gfortran installed. If not there, install the required compilers and librairies using::
    
    sudo apt-get update
    sudo apt-get install gcc-7 g++-7 gfortran-7 libgfortran5

    #On Ubuntu 18.04, use libgfortran3 instead of libgfortran5.

2. Download and install Energyplus 9.4::

    curl -SLO https://github.com/NREL/EnergyPlus/releases/download/v9.4.0/EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh
    chmod +x EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh  #here for Ubuntu 20.04
    sudo echo "y\r" | ./EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh
    rm EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh

3. Install Energym. You can directly install Energym from pypi with pip::

    pip install energym


   Or you can install Energym from its source gitlab repository, with git::

    git clone <energym adress>
    cd <energym main folder>
    python setup.py install --verbose







Docker
--------------------------
For users willing to launch the library within a docker (just for model evaluation and controllers benchmarking), use the file Dockerfile. 

1. Prior to using docker, install it following the instructions:

    - On `Windows <https://docs.docker.com/docker-for-windows/install/>`_. 

    - On `Linux (Ubuntu) <https://docs.docker.com/engine/install/ubuntu/>`_. 

    - On `Mac <https://docs.docker.com/docker-for-mac/install/>`_. 

2. Clone the repository using git::
    
    git clone <energym adress>
    cd <energym main folder>

3. Build and run the container

    - On Windows::
        
        docker build --pull --rm -f "Dockerfile" -t energym:latest "."
        docker run -d -p 80:80 energym:latest

    - On Linux. Use the dockerlauncher in the main repository. Replace the name 'DockerfileFullInstall3.dockerfile' by 'Dockerfile' and execute the launcher::
        
        ./dockerlauncher




