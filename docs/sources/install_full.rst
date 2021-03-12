.. _install_full:

Full Installation
******************


The full installation should be used only by contributors willing to add and develop new buildings models.

Two containers are provided, one with OpenModelica, one with the latest free version of JModelica (2.14). Supported platforms are Linux (Ubuntu) and Windows 10.

**Important note**: Users willing only to compile Energyplus files can skip the installation steps 1 and 4. Users willing only to compile Modelica files can skip steps 2,3,5,6.

**Warning**: The Modelica buildings library is still not fully supported by OpenModelica.


Windows 10
-----------------------
**Note**: The steps 5 and 6 are only needed if you use OpenModelica and Python>=3. JModelica requires a running version of Python 2.7, and 5-6 have to be skipped.


1. Download and install `OpenModelica <https://www.openmodelica.org/>`_ or download JModelica `binaries <https://disq.us/url?url=https%3A%2F%2Fdownloads.modelon.com%2Fdownload%2F%3Fa%3DJMODELICA%3A_xx_BYR7Ndv4fd3-M3M3XSHiyjY&cuid=2163236/>`_.

2. Install Energyplus 9.4; see :ref:`install_min`.

3. Install a  C/C++ compiler (e.g. Visual Studio)

4. Clone the following libraries to your favorite folder::

    git clone https://github.com/lbl-srg/modelica-buildings.git
    git clone https://github.com/ibpsa/modelica-ibpsa.git
    git clone https://github.com/lbl-srg/EnergyPlusToFMU

5. Install 2to3 python package::

    pip install 2to3 

6. Convert EnergyPlusToFMU to python3::

    cd /<favorite_path>/EnergyPlusToFMU
    2to3 . -w
    2to3 . -w  
    #Two times to ensure all python2.7 blocks get converted
    On windows, you may need to change the default compiler address in the .bat files in EnergyplustoFMU/scripts/win to your current C compiler address.

7. Clone Energym::

    git clone <energym adress>
    cd <energym main folder>
    
Then go to the section  :ref:`add_model`.


Linux (Ubuntu)
-----------------------
**Note**: The steps 5 and 6 are only needed if you use OpenModelica and Python>=3. JModelica requires a running version of Python 2.7, and 5-6 have to be skipped.


1. Follow Openmodelica installation `instructions <https://www.openmodelica.org/download/download-linux>`_ or used the provided JModelica zip file in *dependencies* folder.
   The process to install JModelica is given in the dockerfile JModelica.dockerfile.

2. Install Energyplus 9.4; see :ref:`install_min`.

3. Install the following librairies::

    sudo apt-get update && apt-get upgrade -y \
    apt-utils \
    openjdk-11-jre\
    git \
    libc6\
    -y wget gnupg2 lsb-release curl vim

4. Clone the following libraries to your favorite folder::

    git clone https://github.com/lbl-srg/modelica-buildings.git
    git clone https://github.com/ibpsa/modelica-ibpsa.git
    git clone https://github.com/lbl-srg/EnergyPlusToFMU

5. Install 2to3 python package::

    pip install 2to3 

6. Convert EnergyPlusToFMU to python3::

    cd /<favorite_path>/EnergyPlusToFMU
    2to3 . -w
    2to3 . -w  
    #Two times to ensure all python2.7 blocks get converted

7. Clone Energym::

    git clone <energym adress>
    cd <energym main folder>

Then go to the section  :ref:`add_model`.



Docker
-----------------------
We strongly advise to use the provided dockerfiles to build models for linux/darwin platforms. 

1. Prior to using docker, install it following the instructions:

    - On `Windows <https://docs.docker.com/docker-for-windows/install/>`_. 

    - On `Linux (Ubuntu) <https://docs.docker.com/engine/install/ubuntu/>`_. 

    - On `Mac <https://docs.docker.com/docker-for-mac/install/>`_. 

2. Clone the repository using git::
    
    git clone <energym adress>
    cd <energym main folder>

3. Build and run the container. 

    - On Windows::
        
        docker build --pull --rm -f "JModelica.dockerfile" -t energym:latest "."
        docker run -d -p 80:80 energym:latest

    - On Linux. Use the dockerlauncher in the main repository. Replace the name 'DockerfileFullInstall3.dockerfile' by 'JModelica.dockerfile'/'OpenModelica.dockerfile' and execute the launcher::
        
        ./dockerlauncher

    - On Mac (TBD)

Then go to the section  :ref:`add_model`.
