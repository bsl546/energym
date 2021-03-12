# A docker file to compile FMU with EplustoFMU and Energyplus
# Based on python 2.7 and Jmodelica latest open source available version
# Since Jmodelica and python 2.7 are not maintained anymore, we encourage users adding new models
# to use the other dockerfile, with openmodelica and python 3.

FROM ubuntu:18.04


ENV REV_JMODELICA 14023
ENV REV_ASSIMULO 898
##################################################

# Set environment variables
ENV SRC_DIR /usr/local/src


##################################################
# Avoid warnings
# debconf: unable to initialize frontend: Dialog
# debconf: (TERM is not set, so the dialog frontend is not usable.)
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN  apt-get -y update \
    && apt-get install -y apt-utils \
    && apt-get install -y libblas-dev liblapack-dev libblas3 libomp-dev liblapack3 git unzip curl vim


# Install required packages
RUN apt-get update && \
    apt-get install -y \
    ant=1.10.5-3~18.04 \
    autoconf=2.69-11 \
    cmake=3.10.2-1ubuntu2.18.04.1 \
    cython=0.26.1-0.4 \
    g++=4:7.4.* \
    gfortran=4:7.4.0-1ubuntu2.3 \
    libgfortran3 \
    ipython=5.5.0-1 \
    libboost-dev=1.65.1.0ubuntu1 \
    openjdk-8-jdk\
    pkg-config=0.29.1-0ubuntu2 \
    python-dev=2.7.15~rc1-1 \
    python-jpype=0.6.2+dfsg-2 \
    python-lxml \
    python-matplotlib \
    python-nose \
    python-numpy=1:1.13.3-2ubuntu1 \
    python-pip=9.0.* \
    python-scipy=0.19.1-2ubuntu1 \
    python-pandas \
    subversion=1.9.7-4ubuntu1 \
    swig=3.0.12-1 \
    wget=1.19.4-1ubuntu2.2 \
    zlib1g-dev=1:1.2.11.dfsg-0ubuntu2 && \
    rm -rf /var/lib/apt/lists/*

# Install jcc-3.0 to avoid error in python -c "import jcc"
RUN pip install --upgrade pip
RUN ln -s /usr/lib/jvm/java-8-openjdk-amd64 /usr/lib/jvm/java-8-oracle
RUN pip install --upgrade jcc==3.5

RUN export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN export JCC_JDK=/usr/lib/jvm/java-8-openjdk-amd64


WORKDIR /app
ADD . /app

RUN unzip /app/dependencies/JModelica.org-2.14.zip -d $SRC_DIR
RUN chmod -R 755 $SRC_DIR/JModelica.org-2.14
WORKDIR  $SRC_DIR/JModelica.org-2.14
RUN rm -rf build 
RUN mkdir build
RUN cd $SRC_DIR/JModelica.org-2.14/build && \
    ../configure --prefix=/usr/local/JModelica.org-2.14&& \
    make install && \
    #make casadi_interface && \
    rm -rf $SRC_DIR


#################################################################
#Define E+ version 
ENV ENERGYPLUS_INSTALL_VERSION 9-4-0


# Download from github
ENV ENERGYPLUS_DOWNLOAD_URL https://github.com/NREL/EnergyPlus/releases/download/v9.4.0/EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu18.04-x86_64.sh
ENV ENERGYPLUS_DOWNLOAD_FILENAME  EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu18.04-x86_64.sh


RUN rm -rf /var/lib/apt/lists/* 
RUN curl -SLO $ENERGYPLUS_DOWNLOAD_URL 
RUN chmod +x $ENERGYPLUS_DOWNLOAD_FILENAME 
RUN echo "y\r" | ./$ENERGYPLUS_DOWNLOAD_FILENAME 
RUN rm $ENERGYPLUS_DOWNLOAD_FILENAME 
RUN cd /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION 
RUN rm -rf DataSets Documentation ExampleFiles WeatherData MacroDataSets PostProcess/convertESOMTRpgm 
RUN rm -rf PostProcess/EP-Compare PreProcess/FMUParser PreProcess/ParametricPreProcessor PreProcess/IDFVersionUpdater


# Remove the broken symlinks
RUN cd /usr/local/bin \
    && find -L . -type l -delete


#Finally add all other libraries
RUN mkdir /home/libraries
WORKDIR /home/libraries
WORKDIR /home/libraries

#Commented github download because of instabilities when downloading from git
RUN git clone -b v7.0.0  https://github.com/lbl-srg/modelica-buildings.git
#RUN wget https://github.com/lbl-srg/modelica-buildings/releases/download/v7.0.0/Buildings-v7.0.0.zip
#RUN mkdir modelica-buildings
#RUN unzip  Buildings-v7.0.0.zip  && mv 'Buildings 7.0.0'  modelica-buildings/Buildings

RUN git clone https://github.com/ibpsa/modelica-ibpsa.git
RUN git clone https://github.com/lbl-srg/EnergyPlusToFMU


#Add python3 to make the tests
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev


VOLUME /var/simdata/energyplus
WORKDIR /var/simdata/energyplus

ENV ROOT_DIR /usr/local
ENV JMODELICA_HOME $ROOT_DIR/JModelica.org-2.14
ENV SUNDIALS_HOME $JMODELICA_HOME/ThirdParty/Sundials
ENV SEPARATE_PROCESS_JVM /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV MODELICAPATH /usr/local/JModelica.org-2.14/ThirdParty/MSL
ENV PYTHONPATH $PYTHONPATH:$JMODELICA_HOME/Python:$JMODELICA_HOME/Python/pymodelica


CMD [ "/bin/bash" ]