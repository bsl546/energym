.. _install_full:

Full Installation
******************


The full installation should be used only by contributors willing to add and develop new buildings models.

A docker image with the latest opensource version of JModelica (2.14) is stored on dockerhub for users willing to compile with dockers.


Windows 10
-----------------------


1. Download and install JModelica `binaries <https://disq.us/url?url=https%3A%2F%2Fdownloads.modelon.com%2Fdownload%2F%3Fa%3DJMODELICA%3A_xx_BYR7Ndv4fd3-M3M3XSHiyjY&cuid=2163236/>`_.

2. Install Energyplus 9.4; see :ref:`install_min`.

3. Install a  C/C++ compiler (e.g. Visual Studio)

4. Clone the following libraries to your favorite folder::

    git clone https://github.com/lbl-srg/modelica-buildings.git
    git clone https://github.com/ibpsa/modelica-ibpsa.git
    git clone https://github.com/lbl-srg/EnergyPlusToFMU


5. Clone Energym::

    git clone <energym adress>
    cd <energym main folder>
    
Then go to the section  :ref:`add_model`.


Linux (Ubuntu)
-----------------------


1.  Download and install the latest free JModelica version (requires python 2.7)

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


5. Clone Energym::

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

    - On Linux. Use the launcherJmod in the main repository::
        
        ./launcherJmod
        

Then go to the section  :ref:`add_model`.
