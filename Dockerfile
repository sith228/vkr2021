FROM ubuntu:18.04
MAINTAINER Zoreev Mikhail <zoreev@lazyfox.dev>


#Install OpenVino
ENV http_proxy $HTTP_PROXY
ENV https_proxy $HTTPS_PROXY
ARG DOWNLOAD_LINK=http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/l_openvino_toolkit_p_2020.1.023.tgz
ARG INSTALL_DIR=/opt/intel/openvino
ARG TEMP_DIR=/tmp/openvino_installer
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    cpio \
    sudo \
    lsb-release && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p $TEMP_DIR && cd $TEMP_DIR && \
    wget -c $DOWNLOAD_LINK && \
    tar xf l_openvino_toolkit*.tgz && \
    cd l_openvino_toolkit* && \
    sed -i 's/decline/accept/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    rm -rf $TEMP_DIR
RUN $INSTALL_DIR/install_dependencies/install_openvino_dependencies.sh

#BIES


#Install requirements
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev curl gnupg

ADD requirements.txt /server/requirements.txt
RUN pip3 install -r "server/requirements.txt"
RUN pip3 --no-cache-dir install torch
RUN pip3 install torchvision

#Copy files
RUN mkdir /server/common
ADD /common /server/common

RUN mkdir /server/tools
ADD /tools /server/tools

ADD Run.sh /server/Run.sh
ADD image_saver_server.py /server/image_saver_server.py

RUN mkdir /server/files


#Expose port
EXPOSE 5000

#Server start
WORKDIR /server
ENTRYPOINT ["bash"]
CMD ["./Run.sh"]