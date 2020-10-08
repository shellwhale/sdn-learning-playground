#!/bin/bash

docker build -t gracious-ritchie:iperf3 -f Dockerfile.iperf3 .
docker build -t gracious-ritchie:frrouting-debian -f Dockerfile.frrouting-debian .