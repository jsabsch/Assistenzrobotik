#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import force
import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Vector3Stamped

MAX_FORCE = 1   # in Joule ?
MASSES = [1,1,1,1,1,1]
LENGTHS = [0.36, 0.42, 0.4]


class Velocity():

    def __init__(self):
        rospy.Subscriber("/arm_state", JointState, self.subscribe_arm_state)
        self.max_vel_pub = rospy.Publisher("/maxVelocity", Vector3Stamped, queue_size=1)
        self.forceCalc = force.force_calculator(MAX_FORCE, MASSES, LENGTHS)


    def subscribe_arm_state(self, msg):
        if isinstance(msg, JointState):
            q = msg.position
            direction = [1, 0, 0]  # FIXME
            maxVelocityScalar, m_u = self.forceCalc.calc_max_speed(q, direction)
            msg = self.toMessage(maxVelocityScalar)
            self.max_vel_pub.publish(msg)
    
    def toMessage(self, maxVelocity):
        msg = Vector3Stamped()
        v = msg.vector
        v.x = v.y = v.z = maxVelocity
        return msg

if __name__ == '__main__':
    rospy.init_node('velocityCalculation')
    rate = rospy.Rate(10)  # 10hz

    vel = Velocity()

    print("velocityCalculation has started.")
    while not rospy.is_shutdown():
        rate.sleep()

    rospy.spin()
