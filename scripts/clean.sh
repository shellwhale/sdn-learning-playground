#!/bin/bash

a=`sudo docker ps -aq`
sudo docker stop $a
sudo docker rm $a
sudo mn -c