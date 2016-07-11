#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Vector3Stamped

import velocity

def __is_on_target(pose):
    """ TODO: get arm state. if is nearly the same as target position, set on_target true
    """
    #pass
    return True
    


def rotate_path(path, index):
    """ choose the current target position.
    """
    if on_target:
        index += 1
        if index >= len(path):
            index = 0
    
    global right_pub
    global velocityCalculator
    pose = path[index]
    velocityCalculator.setDir((pose.pose.position.x, pose.pose.position.y, pose.pose.position.z))
    
    __fill_header(pose.header)
    right_pub.publish(pose)
    
    return index

def __init_pose_array():
    """ define the standard path for the robot.
    """
    path = []
    f = 0.2
    path.append(__pose(-f, 0, -f,     0, 0, 0, 0))
    path.append(__pose(+f, 0, -f,     0, 0, 0, 0))
    path.append(__pose(+f, 0, +f,     0, 0, 0, 0))
    path.append(__pose(-f, 0, +f,     0, 0, 0, 0))
    return path
    
def __pose(px,py,pz,ow,ox,oy,oz):
    """ Fill a geometry_msgs/Pose.
    """
    
    p = Pose()
    p.position.x = px
    p.position.y = py
    p.position.z = pz
    p.orientation.w = ow
    p.orientation.x = ox
    p.orientation.y = oy
    p.orientation.z = oz
    
    ps = PoseStamped()
    ps.pose = p
    
    return ps

def __maxVelocity(scalarValue):
    msg = Vector3Stamped()
    __fill_header(msg.header)
    msg.vector.x = msg.vector.y = msg.vector.z = scalarValue

def __fill_header(header):
    """ Fill a header with a sequence number, a time stamp and the frame id.
    """
    global seq
    
    header.seq = seq
    seq += 1
    
    header.stamp = rospy.Time.now()
    header.frame_id = "/table"
    
    return header

def tmp():
    # TODO: NUR ZUM TESTEN
     
     
    global tmp_counter
    tmp_counter += 1
    
    if tmp_counter >= 20:
        tmp_counter = 0
        return True

    return False

if __name__ == '__main__':

    rospy.init_node('assistenzrobotik')
    rate = rospy.Rate(10)  # 10hz

    standard_path = __init_pose_array()

    right_pub = rospy.Publisher("/targetPos", PoseStamped, queue_size=1)

    velocityCalculator = velocity.Velocity()

    index = 0
    seq = 0
    on_target = False
    
    tmp_counter = 0 # TODO: NUR ZUM TESTEN
    
    print("Start successful.")
    
    while not rospy.is_shutdown():
        index = rotate_path(standard_path, index)
        on_target = tmp()   # TODO: NUR ZUM TESTEN
        rate.sleep()

    print("\nShutdown.")