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
from move_canopy.msg import push, confirm

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
offset_y = 0.0
offset_z = 0.0

class manipulator:

    def __init__(self):
        self.confirm_pub = rospy.Publisher("grab_status",confirm)
        self.target_sub = rospy.Subscriber("push", push, self.push_callback)

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
                time.sleep(0.5)

            else:
                print('No IK Solution found for '+ str(target_position[i,:]))

    def move_arm(x0, y0, z0, x1, y1, z1):
        # go to x y z + threshold
        
        traj0 = linear_path( x0, y0 , z0, x1, y1, z1)
        execute(traj0, gripper = GRIPPER_LOSE)
        traj1 = linear_path(x1, y1, z1, offset_x, offset_y, offset_z)
        execute(traj1, gripper = GRIPPER_LOSE)
        time.sleep(0.1)

    def push_callback(data):
        move_arm(data.x0, data.y0, data.z0, data.x1, data.y1, data.z1)
        msg = confirm()
        msg.confirm = True
        self.confirm_pub.publish(msg)

def main():
    arm = manipulator()
    rospy.init_node('ARM', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
