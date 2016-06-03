#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose

def subscribe_arm_state(msg):
    pass

if __name__ == '__main__':

    rospy.init_node('fusion_hack4')
    
    rospy.Subscriber("/vrep/LBR_iiwa_14_RB20/jointStatus", JointState, subscribe_arm_state)
    right_pub = rospy.Publisher("target_pose", Pose, queue_size=1)
    
    rospy.spin()