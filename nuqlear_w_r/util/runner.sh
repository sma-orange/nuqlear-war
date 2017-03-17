#!/bin/bash

# Script to run NuQ from a Python sub-process with a small amount of elegance
# Author: Ben Smith [ben.smith@orange.com]
# part of the "NuQleaR War" release, which is version 0.5.x
# TODO: return something meaningful on success or failure
# TODO: fix paths for Cube
# TODO: check env is active and options ok?
# these are dev laptop paths
source "/home/ben/virtuals/vnuq/bin/activate"
# dev laptop paths
nohup /home/ben/virtuals/vnuq/bin/python3.5 /home/ben/PycharmProjects/nuqlear_war/nuq/nuqlear.py $1 &
sleep 1
kill -INT $!
