#!/bin/bash

for container_directory in *; do
    if [ -d "${container_directory}" ]; then
        docker build -t "gracious-ritchie:${container_directory}" "./${container_directory}"
    fi
done