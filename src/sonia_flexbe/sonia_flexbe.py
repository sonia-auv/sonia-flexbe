#! /usr/bin/env python2
import rospy

class SoniaFlexbe:

    def __init__(self):
        rospy.init_node('sonia_flexbe')
        rospy.spin()

if __name__ == '__main__':
    SoniaFlexbe()