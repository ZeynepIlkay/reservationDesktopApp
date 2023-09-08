#!/bin/bash

xhost +local:docker

docker run -e TZ=Europe/Istanbul -it --rm -e DISPLAY=:0 --network="host" --name gui_container gui_image

xhost -local:docker