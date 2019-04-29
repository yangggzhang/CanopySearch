"""
Example for using Analytic IK on 5dof locobot
"""

import sys
import time

import numpy as np
import rospy
from sensor_msgs.msg import JointState
from analytic_ik import AnalyticInverseKinematics

ROSTOPIC_SET_ARM_JOINT = '/goal_dynamixel_position'

def home_arm(pub):
    rospy.loginfo('Going to arm home pose')
    set_arm_joint(pub, np.zeros(5))
    rospy.sleep(5)

def set_arm_joint(pub, joint_target):
    joint_state = JointState()
    joint_state.position = tuple(joint_target)
    pub.publish(joint_state)

def main():
    rospy.init_node('analytic_ik_example', anonymous=True)

    pub = rospy.Publisher(ROSTOPIC_SET_ARM_JOINT,
                          JointState, queue_size=1)
    ik_solver = AnalyticInverseKinematics()
    rospy.sleep(2)
    home_arm(pub)

    n_samples_x = 3
    n_samples_y = 3

    min_x = 0.20
    max_x = 0.30
    min_y = -0.15
    max_y = 0.15
    fixed_z = 0.20

    x = np.linspace(min_x, max_x, n_samples_x)
    y = np.linspace(min_y, max_y, n_samples_y)
    xv, yv = np.meshgrid(x, y)
    x = xv.flatten()
    y = yv.flatten()
    z = fixed_z * np.ones(len(x))
    target_position = np.array([x,y,z]).T

    for i in range(len(x)):

        target_joint = ik_solver.ik(target_position[i,0], target_position[i,1], target_position[i,2], alpha=-np.pi/2)

        if target_joint is not None:
            target_joint.append(0.0)

            set_arm_joint(pub, target_joint)
            time.sleep(4)

        else:
            print('No IK Solution found for '+ str(target_position[i,:]))

    home_arm(pub)


if __name__ == "__main__":
    main()
