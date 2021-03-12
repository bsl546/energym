FROM ubuntu:focal


#Non interactive to avoid tz questions
ARG DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV SRC_DIR /usr/local/src

RUN apt-get update && apt-get upgrade -y \
    apt-utils \
    openjdk-11-jre\
    git \
    libc6\
    -y wget gnupg2 lsb-release curl vim


RUN for deb in deb deb-src; do echo "$deb http://build.openmodelica.org/apt `lsb_release -cs` nightly"; done |  tee /etc/apt/sources.list.d/openmodelica.list
RUN wget -q http://build.openmodelica.org/apt/openmodelica.asc -O- |  apt-key add -

# Update index (again)
RUN apt-get update
RUN apt install -y openmodelica
RUN for PKG in `apt-cache search "omlib-.*" | cut -d" " -f1`; do apt-get install -y "$PKG"; done 


RUN apt-get install -y python3-pip \
    python3 \
    python3-setuptools \
    python3-pip \
    && pip3 install --upgrade pip


# Install OMPython 
RUN pip install 2to3 


# #####################################################################################################################
# #Installing E+
# #Define E+ version 
ENV ENERGYPLUS_INSTALL_VERSION 9-4-0


# # Download from github
ENV ENERGYPLUS_DOWNLOAD_URL https://github.com/NREL/EnergyPlus/releases/download/v9.4.0/EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh
ENV ENERGYPLUS_DOWNLOAD_FILENAME  EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh

RUN rm -rf /var/lib/apt/lists/* 
RUN curl -SLO $ENERGYPLUS_DOWNLOAD_URL 
RUN chmod +x $ENERGYPLUS_DOWNLOAD_FILENAME 
RUN echo "y\r" | ./$ENERGYPLUS_DOWNLOAD_FILENAME 
RUN rm $ENERGYPLUS_DOWNLOAD_FILENAME 
RUN cd /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION 
RUN rm -rf DataSets Documentation ExampleFiles WeatherData MacroDataSets PostProcess/convertESOMTRpgm 
RUN rm -rf PostProcess/EP-Compare PreProcess/FMUParser PreProcess/ParametricPreProcessor PreProcess/IDFVersionUpdater

# # Remove the broken symlinks
RUN cd /usr/local/bin \
    && find -L . -type l -delete

# #Finally install te required packages for energym
WORKDIR /home/libraries
RUN git clone https://github.com/lbl-srg/modelica-buildings.git
RUN git clone https://github.com/ibpsa/modelica-ibpsa.git
RUN git clone https://github.com/lbl-srg/EnergyPlusToFMU


# WORKDIR /app
ADD . /app
RUN chmod -R 777 /app  #To be able to run openmodelica inside


# #Install our python packages
WORKDIR /app
RUN  pip install -r requirements.txt --verbose
RUN pip install -e . --verbose

# Create a user profile "openmodelicausers" inside the docker container as we should run the docker container as non-root users.
# Issues otherwise with OMPython
RUN useradd -m -s /bin/bash openmodelicausers

#Convert E+toFMU to python3, run two times to have all cleanup
WORKDIR /home/libraries/EnergyPlusToFMU
RUN 2to3 . -w
RUN 2to3 . -w  



CMD [ "/bin/bash" ]





