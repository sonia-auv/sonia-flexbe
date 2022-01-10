#!/bin/bash

cd

cd ros_sonia_ws/

# Build the catkin workspace
catkin_make

# Source the workspace
source devel/setup.bash

roslaunch sonia_flexbe sonia_flexbe_setup.launch