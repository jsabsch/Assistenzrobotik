#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose

def subscribe_arm_state(msg):
    """ Get the Pose of the arms last joint and control the target positions.
    
    Compare the arms pose to the current target position and switch to the next one, if the are similar 
    enough.
    
    """
    
    global on_target

    if __is_on_target(msg.pose):
        on_target = True
    else:
        on_target = False
 
def __is_on_target(pose):
    """ TODO: get arm state. if is nearly the same as target position, set on_target true
    """
    pass
    


def rotate_path(path, index):
    """ choose the current target position.
    """
    if on_target:
        index += 1
        if index >= len(path):
            index = 0
    
    global right_pub
    right_pub.publish(__fill_header(path[index]))
    
    return index

def __init_pose_array():
    """ define the standard path for the robot.
    """
    path = []
    path.append(__pose(0,0,0.2, 0,0,0,0))
    path.append(__pose(0,0,0,0, 0,0,0))
    path.append(__pose(0,0,0.2, 0,0,0,0))
    path.append(__pose(0,0.2,0.2, 0,0,0,0))
    path.append(__pose(0,0.2,0, 0,0,0,0))
    path.append(__pose(0,0.2,0.2, 0,0,0,0))
    path.append(__pose(0.2,0.2,0.2, 0,0,0,0))
    path.append(__pose(0.2,0.2,0, 0,0,0,0))
    path.append(__pose(0.2,0,0.2, 0,0,0,0))
    path.append(__pose(0.2,0,0, 0,0,0,0))
    path.append(__pose(0.2,0,0.2, 0,0,0,0))
    
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

def __fill_header(pose_stamped):
    """ Fill a pose_stampeds header with a sequence number, a time stamp and the frame id.
    """
    
    global seq
    
    pose_stamped.header.seq = seq
    seq += 1
    
    pose_stamped.header.stamp = rospy.Time.now()
    pose_stamped.header.frame_id = "/table"
    
    return pose_stamped

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
    rate = rospy.Rate(10) # 10hz

    standard_path = __init_pose_array()
        
    rospy.Subscriber("/vrep/LBR_iiwa_14_RB20/jointStatus", JointState, subscribe_arm_state)
    right_pub = rospy.Publisher("target_pose", PoseStamped, queue_size=1)
    
    index = 0
    seq = 0
    on_target = False
    
    tmp_counter = 0 # TODO: NUR ZUM TESTEN
    
    while not rospy.is_shutdown():
        index = rotate_path(standard_path, index)
        on_target = tmp()   # TODO: NUR ZUM TESTEN
        rate.sleep()

    rospy.spin()