# Download from docker hub an image with Ubuntu 18.04, Jmodelica 2.14, python2.7, python3.6

FROM  bsl546/docker_jmod:v01
WORKDIR /app
ADD . /app

RUN python3 setup.py install


CMD [ "/bin/bash" ]
