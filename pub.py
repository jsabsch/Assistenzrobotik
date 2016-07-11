import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose

def pose():
    msg = PoseStamped()
    p = Pose()
    p.position.x = 0.00537528842688
    p.position.y = 0.670555531979
    p.position.z = 0.766715943813
    o = p.orientation
    o.x = -0.000425785779953
    o.y = 0.642718672752
    o.z = -0.000314554636134
    o.w = 0.766102194786

    msg.pose = p
    return msg
rospy.init_node('assistenzrobotik_pub')
pub = rospy.Publisher("/targetPos", PoseStamped, queue_size=1)
pub.publish(pose())
rospy.spin()