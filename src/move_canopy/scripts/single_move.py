"""
Example for using Analytic IK on 5dof locobot
"""

import sys
import time

import numpy as np
import rospy
from sensor_msgs.msg import JointState
from analytic_ik import AnalyticInverseKinematics
from rospy_tutorials.msg import Floats
from std_msgs.msg import Empty, Bool
from move_canopy.srv import MovePos, MovePosResponse

ROSTOPIC_SET_ARM_JOINT = '/goal_dynamixel_position'
ROSTOPIC_SET_PAN_JOINT = '/pan/command'
ROSTOPIC_SET_TILT_JOINT = '/tilt/command'
ROSTOPIC_OPEN_GRIPPER = '/gripper/open'
ROSTOPIC_CLOSE_GRIPPER = '/gripper/close'

ROSTOPIC_SET_ARM_JOINT = '/goal_dynamixel_position'

pub = rospy.Publisher(ROSTOPIC_SET_ARM_JOINT, JointState, queue_size=1)
gripper_open_pub = rospy.Publisher(ROSTOPIC_OPEN_GRIPPER, Empty, queue_size=1)
gripper_close_pub = rospy.Publisher(ROSTOPIC_CLOSE_GRIPPER, Empty, queue_size=1)

ik_solver = AnalyticInverseKinematics()

z_threshold = 0.1
GRIPPER_LOSE = 1.0
GRIPPER_TIGHT = -0.5

offset_x = 0.2
offset_y = -0.15
offset_z = 0.1

def open_gripper(pub):
    empty_msg = Empty()
    rospy.loginfo('Opening gripper')
    pub.publish(empty_msg)

def close_gripper(pub):
    empty_msg = Empty()
    rospy.loginfo('Closing gripper')
    pub.publish(empty_msg)

def home_arm(pub):
    rospy.loginfo('Going to arm home pose')
    set_arm_joint(pub, np.zeros(5))
    rospy.sleep(1)

def set_arm_joint(pub, joint_target):
    joint_state = JointState()
    joint_state.position = tuple(joint_target)
    pub.publish(joint_state)

def linear_path(min_x, min_y, min_z , max_x, max_y, max_z, n_samples = 5):
    x = np.linspace(min_x, max_x, n_samples)
    y = np.linspace(min_y, max_y, n_samples)
    xv, yv = np.meshgrid(x, y)
    x = xv.flatten()
    y = yv.flatten()
    z = np.linspace(min_z, max_z, len(x))
    target_position = np.array([x,y,z]).T
    return target_position

def execute(target_position, gripper =  0.0, alpha = 0.0):
    n, _ = target_position.shape
    for i in range(n):

        target_joint = ik_solver.ik(target_position[i,0], target_position[i,1], target_position[i,2], alpha)

        if target_joint is not None:
            target_joint.append(0.0)

            set_arm_joint(pub, target_joint)
            time.sleep(0.1)

        else:
            print('No IK Solution found for '+ str(target_position[i,:]))

def update_position(x, y, z):
    offset_x = x
    offset_y = y
    offset_z = z


def move_arm(x, y, z):
    # go to x y z + threshold
    
    traj = linear_path( offset_x, offset_y , offset_z, x, y, z + z_threshold)
    execute(traj, gripper = GRIPPER_LOSE)
    print("finish moving")
    update_position(x, y, z)
    time.sleep(0.1)


def callback(req):
    move_arm(req.x, req.y, req.z)
    print(req.x, req.y, req.z)
    resp = MovePosResponse()
    resp.reached = True
    return resp
    # grab(data.data[0],data.data[1],data.data[2])

def main():
    rospy.init_node('ARM', anonymous=True)
    print("start")
    s = rospy.Service('move_arm', MovePos, callback)
    # home_arm(pub)
    # close_gripper(pub)
    # rospy.Subscriber("test", Bool, callback, queue_size= 1)
    # rospy.Subscriber("floats", Floats, callback, queue_size= 1)
    # grab(-0.0630809, -0.249283, 0.146288)
    print("finish")
    rospy.spin()
    # home_arm(pub)
    


if __name__ == "__main__":
    main()
