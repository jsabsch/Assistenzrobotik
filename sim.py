from morse.builder import *

atrv = ATRV()

arm = KukaLWR()
arm.translate(x=0.1850, y=0.2000, z=0.9070)
arm.rotate(x=1.5708, y=1.5708)
atrv.append(arm)

#gripper = Gripper()
#gripper.translate(z=1.2800)
#arm.append(gripper)

motion = MotionVW()
motion.translate(z=0.3)
atrv.append(motion)

pose = Pose()
pose.translate(z=0.83)
atrv.append(pose)

pose.add_stream('ros')
motion.add_stream('ros')
arm.add_stream('ros')
#gripper.add_stream('ros')

env = Environment('indoors-1/indoor-1')
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])
