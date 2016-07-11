import force
import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Vector3Stamped


def subscribe_arm_state(msg):
    if isinstance(msg, JointState):
        q = msg.position
        direction = [1, 0, 0]  # FIXME
        maxVelocityScalar = forceCalc.calc_max_speed(q, direction)
        msg = toMessage(maxVelocityScalar)
        pub.publish(msg)


def toMessage(maxVelocity):
    msg = Vector3Stamped()
    v = msg.vector
    v.x = v.y = v.z = maxVelocity
    return msg


if __name__ == '__main__':
    rospy.init_node('velocityCalculation')
    rate = rospy.Rate(10)  # 10hz

    rospy.Subscriber("/arm_state", JointState, subscribe_arm_state)
    pub = rospy.Publisher("/maxVelocity", Vector3Stamped, queue_size=1)
    forceCalc = force.force_calculator()
    # while not rospy.is_shutdown():
    #     rate.sleep()

    rospy.spin()
