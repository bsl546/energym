# Download from docker hub an image with Ubuntu 20.04 and python 3.7
#Base image for running models (not for compiling them)

FROM  bsl546/docker_energym_base:v02
WORKDIR /app
ADD . /app

RUN python setup.py install


CMD [ "/bin/bash" ]
