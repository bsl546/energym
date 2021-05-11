#A light docker file for running the models without compiling

FROM ubuntu:20.04

#Non interactive to avoid tz questions
ARG DEBIAN_FRONTEND=noninteractive


RUN apt-get update \
    && apt-get install -y python3-pip python3-dev  curl libx11-6 libexpat1 libxml2\
    vim gcc-7 g++-7 gfortran-7 libgfortran5\
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip


###########################################################
#Installing E+
#Define E+ version 
ENV ENERGYPLUS_INSTALL_VERSION 9-5-0


# Download from github
ENV ENERGYPLUS_DOWNLOAD_URL https://github.com/NREL/EnergyPlus/releases/download/v9.5.0/EnergyPlus-9.5.0-de239b2e5f-Linux-Ubuntu20.04-x86_64.sh
ENV ENERGYPLUS_DOWNLOAD_FILENAME  EnergyPlus-9.5.0-de239b2e5f-Linux-Ubuntu20.04-x86_64.sh

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




###########################################################
#Installing python modules
WORKDIR /app

ADD . /app
RUN  python setup.py install --verbose

###########################################################


VOLUME /var/simdata/energyplus
WORKDIR /var/simdata/energyplus

CMD [ "/bin/bash" ]







