#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import force
import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Vector3Stamped
from geometry_msgs.msg._PoseStamped import PoseStamped

import math

MAX_FORCE = 1  # in Joule ?
MASSES = [1, 1, 1, 1, 1, 1]
LENGTHS = [0.36, 0.42, 0.4]


class Velocity():
    def __init__(self, pub):
        rospy.Subscriber("/arm_state", JointState, self.subscribe_arm_state)
        self.move_pub = pub
        
        self.max_vel_pub = rospy.Publisher("/maxVelocity", Vector3Stamped, queue_size=1)
        self.forceCalc = force.force_calculator(MAX_FORCE, MASSES, LENGTHS)
        
        self.direction = [1,0,0]
        self.pose = PoseStamped()
        
        self.last_pos = [0,0,0]
        self.current_pos = [0,0,0]
        
        self.maxVelScalar = 0

    def subscribe_arm_state(self, msg):
        if isinstance(msg, JointState):
            q = msg.position
            maxVelocityScalar, m_u = self.forceCalc.calc_max_speed(q, self.direction)
            
            if math.isnan(maxVelocityScalar):
                print("is nan...")
                maxVelocityScalar = 0
            
            self.maxVelScalar = maxVelocityScalar
            
#             msg = self.toMessage(maxVelocityScalar)
# 
#             self.max_vel_pub.publish(msg)
#             self.move_pub.publish(self.pose)

    def toMessage(self, maxVelocity):
        msg = Vector3Stamped()
        v = msg.vector
        v.x = v.y = v.z = maxVelocity
        return msg
    
    def setDir(self, pose):
        self.pose = pose
        self.direction = self.__calc_move(pose.pose.position)

    def __calc_move(self, pos):
        if (pos.x, pos.y, pos.z) != self.current_pos:
            self.last_pos = self.current_pos
            self.current_pos = (pos.x, pos.y, pos.z)
        
        dir = (self.current_pos[0] - self.last_pos[0], self.current_pos[1] - self.last_pos[1], self.current_pos[2] - self.last_pos[2])
        l = math.sqrt(sum([d**2 for d in dir]))
        if l == 0:
            return (0,0,0)
        
        return (dir[0] / l , dir[1] / l , dir[2] / l)

    def update(self):
        msg = self.toMessage(self.maxVelScalar)

        self.max_vel_pub.publish(msg)
        self.move_pub.publish(self.pose)


if __name__ == '__main__':
    rospy.init_node('velocityCalculation')
    rate = rospy.Rate(10)  # 10hz

    vel = Velocity()

    print("velocityCalculation has started.")
    while not rospy.is_shutdown():
        rate.sleep()

    rospy.spin()
