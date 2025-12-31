#!/bin/bash

#set -x
image=andrew/att-modem

version=$(date '+%Y%m%d')

docker images | grep ${image}
set -x 
docker build ${1} \
    --tag ${image}:${version} \
    --no-cache \
    --progress plain . && \
docker tag ${image}:${version} ${image}:latest && \
docker images | grep ${image}
