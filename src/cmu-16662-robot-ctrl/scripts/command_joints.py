#!/usr/bin/env python
"""
Example for commanding joints
"""

import sys

import numpy as np
import rospy
from sensor_msgs.msg import JointState
from ar_track_alvar_msgs.msg import AlvarMarkers
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
from F_K1 import FK

ROSTOPIC_SET_ARM_JOINT = '/goal_dynamixel_position'
pos_3d_cam = []
pos_3d_world = []
pos_2d = np.ones(3)
pos = [0.0,0.0,1.0]
bridge = CvBridge()

def plan_trajectory(waypoints, num):
    traj = np.zeros(5)
    finalTraj = [traj]
    current_step = np.zeros(5)
    for next_step in waypoints:
        step_size = (next_step - current_step)/num
        for j in range(num):
            current_step = current_step + step_size
            # traj = np.concatenate((traj, current_step))
            finalTraj.append(current_step)
    finalTraj = np.stack(finalTraj)
    # print(finalTraj.shape)
    return finalTraj

def home_arm(pub):
    rospy.loginfo('Going to arm home pose')
    set_arm_joint(pub, np.zeros(5))
    rospy.sleep(5)


def set_arm_joint(pub, joint_target):
    joint_state = JointState()
    joint_state.position = tuple(joint_target)
    pub.publish(joint_state)


def get_artag_pos_in_world(forward_kinematic, joint):
    # fk from base to artag
    bd_pose = forward_kinematic.get_bdbox_pose(joint)
    return bd_pose[4][0:3,3]
    

def sub_callback(AlvarMarkers):
    global pos_3d_cam
    global pos
    if len(AlvarMarkers.markers)>0:
        pos = [AlvarMarkers.markers[0].pose.pose.position.x,
        AlvarMarkers.markers[0].pose.pose.position.y,
        AlvarMarkers.markers[0].pose.pose.position.z]
    else:
        pos = []

    # ori = marker.pose.orientation
    

def img_callback(Imgs):
    global pos_2d
    cv_image = bridge.imgmsg_to_cv2(Imgs,"bgr8")
    # print(pos_2d[0]/pos_2d[2])
    cv2.circle(cv_image,((pos_2d[0]/pos_2d[2]).astype(int),(pos_2d[1]/pos_2d[2]).astype(int)),8,(0,0,255))
    cv2.imshow("Image",cv_image)
    cv2.waitKey(3)
    # cv2.destroyAllWindows()
    # print(np.int8(np.array(Imgs.data))) 

def main():
    global pos_3d_cam
    global pos_3d_world
    global pos_2d
    global pos
    

    intrinsic_matrix = [ 
        [614.357421875,  0.0,            310.2319641113281],
        [0.0,            614.494140625,  244.32691955566406], 
        [0.0,            0.0,            1.0]
    ]

    intrinsic_matrix = np.array(intrinsic_matrix)

    target_joints = [
        [0.408, 0.721, -0.471, -0.8, -0.120],
        [0.08, 0.21, -0.1, -0.7, -0.340],
        [0.08, 0.21, -0.3, -0.6, -0.340],
        [-0.48, -0.31, 0.4, -0.7, 0.30],
        [-0.208, -0.31, 0.4, -0.7, 0.30],
        [0.545, 0, 0.23, -1.1, -0.40],
        [0.35, -0.41, 0.17, -0.9, 0.30],
        [0.25, -0.41, 0.17, -0.9, 0.20],
        [-0.15, -0.41, 0.17, -0.9, -0.230],
        [-0.25, -0.41, 0.17, -0.9, -0.30],
        [-0.28, -0.41, 0.17, -0.9, -0.10],
        [0,0,0,-0.9,0],
        [-0.1,0,0,-1.1,0],
        [0.1,0,0,-1.3,0],
        [0,0,0,-1.6,0]
    ]

    a_cuboid_pos = [[-0.08960255235433578, 0.00038756412686780095, 0.1852499544620514], 
    [-0.08553405851125717, -0.022655948996543884, 0.30225038528442383], 
    [-0.0628858134150505, -0.15112994611263275, 0.4002501368522644], 
    [-0.041500769555568695, -0.27241623401641846, 0.41218096017837524], 
    [-0.02877490222454071, -0.3440069556236267, 0.40787506103515625], 
    [-0.00696568563580513, -0.3876582384109497, 0.4004143178462982], 
    [-0.034540317952632904, -0.39252030849456787, 0.4004143476486206]]

    a_cuboid_orient = [[-1.5707964897155762, -0.17453302443027496, -1.5707964897155762], 
    [1.1720808288373519e-05, -5.874709677300416e-05, 0.17451781034469604], 
    [-1.5707964897155762, -0.17453274130821228, -1.5707964897155762], 
    [1.5681496858596802, 0.17453262209892273, 1.5715703964233398], 
    [-1.5707976818084717, 1.3962639570236206, -1.5707969665527344], 
    [1.5707966089248657, 0.1745329648256302, 3.141536235809326], 
    [1.5707966089248657, 0.1745329648256302, 3.141536235809326]] 

    a_cuboid_dim = [[0.0525 , 0.10183, 0.10218], 
    [0.0369    , 0.046     , 0.21518999], 
    [0.0369    , 0.046     , 0.21518999], 
    [0.046634, 0.04402 , 0.076364], 
    [0.05525, 0.07305, 0.1025 ], 
    [0.014001, 0.021301, 0.0553  ], 
    [0.014001, 0.021301, 0.0553  ]]

    joint_values = [-1.3962633609771729, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    joint_poses = [[-0.08960248529911041, 0.00038749544182792306, 0.15900005400180817], 
    [-0.08960256725549698, 0.00038756412686780095, 0.20025001466274261], 
    [-0.08092013746500015, -0.04885284602642059, 0.40025001764297485], 
    [-0.046155862510204315, -0.2460113912820816, 0.40025007724761963], 
    [-0.03511735051870346, -0.3080369830131531, 0.40025001764297485], 
    [-0.046203020960092545, -0.3839654326438904, 0.4052642583847046], 
    [0.0030373409390449524, -0.3752831220626831, 0.4052642583847046]] 

    ar_pose_save = np.load("/home/zy/Documents/RobotAutonomy/catkin_ws/src/cmu-16662-robot-ctrl/scripts/ar_pose_save.npy")
    print(ar_pose_save)
    
    forward_kinematic = FK(joint_values,joint_poses,a_cuboid_pos,a_cuboid_orient)
    # print(get_artag_pos_in_world(forward_kinematic, target_joints[0]))

    rospy.init_node('command_joints_example', anonymous=True)
    pub = rospy.Publisher(ROSTOPIC_SET_ARM_JOINT,
                          JointState, queue_size=1)
    sub = rospy.Subscriber("/ar_pose_marker", AlvarMarkers, sub_callback)
    sub_img = rospy.Subscriber("/camera/color/image_raw", Image, img_callback)

    # extrinsic = np.load("extrinsic.npy")
    extrinsic = np.load("/home/zy/Documents/RobotAutonomy/catkin_ws/src/cmu-16662-robot-ctrl/scripts/extrinsic_2.npy") 
    M = intrinsic_matrix.dot(extrinsic)

    rospy.sleep(2)
    
    raw_input("Robot ready to move to HOME POSITION. Press Enter to continue.")
    print("Robot moving. Please wait.")
    home_arm(pub)
    rospy.sleep(5)
    

    for i in range(len(target_joints)):
        joint = target_joints[i]
        set_arm_joint(pub, joint)
        print(joint)
        rospy.sleep(5)
        # raw_input("Robot ready to move to START POSITION. Press Enter to continue.")
        if len(pos)>0:
            threed_pose = get_artag_pos_in_world(forward_kinematic,joint)
            # threed_pose = np.array(ar_pose_save[i][0])
            print(threed_pose)
            threed_pose = np.insert(threed_pose,3,1,axis=0)
            pos_calculate = extrinsic.dot(threed_pose)
            print("pos_calculate",pos_calculate)
            print("pos",pos)
            print("error",pos_calculate-pos)
            # pos_2d = M.dot(threed_pose)
            pos_2d = intrinsic_matrix.dot(pos_calculate.transpose())
            # pos_2d = intrinsic_matrix.dot(np.array(pos).transpose())
            print(pos_2d[0]/pos_2d[2])
            # pos_3d_world.append(get_artag_pos_in_world(forward_kinematic,joint))
            pos_3d_world.append(threed_pose[:3])
            pos_3d_cam.append([pos[0], pos[1], pos[2]])
            print("Finished sampling. Robot start moving. Please wait.")
        

    # convert pos_3d_cam to 2d pos in image
    
    intrinsic_matrix = np.array(intrinsic_matrix)
    pos_3d_cam = np.vstack(pos_3d_cam)
    pos_3d_world = np.array(pos_3d_world)

    np.save("pos_3d_cam.npy",pos_3d_cam)
    
    # pos_3d_cam = np.load("pos_3d_cam.npy")
    # pos_zs = pos_3d_cam[:,2]
    # pos_2d =  intrinsic_matrix.dot(pos_3d_cam)
    # pos_3d = np.array(pos)
    print(pos_3d_cam.shape)
    pos_2d =  intrinsic_matrix.dot(pos_3d_cam.transpose())
    # pos_2d =  intrinsic_matrix.dot(pos_3d_cam)
    pos_2d[0,:] = pos_2d[0,:]/pos_2d[2,:]
    pos_2d[1,:] = pos_2d[1,:]/pos_2d[2,:]
    print(pos_2d[:2,:])

    # forward_kinematic = FK(joint_values,joint_poses,a_cuboid_pos,a_cuboid_orient)


    
    np.save("pos_3d_world.npy",pos_3d_world)
    np.save("pos_2d.npy",pos_2d)
    
    # pos_3d_world = np.load("pos_3d_world.npy")
    print(pos_3d_world.shape)
    # pos_2d = np.load("pos_2d.npy")
    print(pos_2d.shape)
    # pos_3d_world = pos_3d_world.transpose()
    # print(pos_3d_world[:,:])
    # print(pos_2d)

    pos_3d_world = pos_3d_world.astype(np.float64)
    pos_2d = pos_2d.astype(np.float32)
    # pos_3d_world = pos_3d_world.transpose()
    pos_2d = pos_2d.transpose()

    
    _,ir_rvec, ir_tvec, ir_inliers = cv2.solvePnPRansac(pos_3d_world, pos_2d[:,:2],intrinsic_matrix,np.array([]))
    
    ir_rvec = np.array(ir_rvec)
    ir_tvec = np.array(ir_tvec)
    # ir_tvec = ir_tvec.transpose()

    print (ir_rvec)
    print (ir_tvec)

    extrinsic = np.zeros((3,4))
    # extrinsic[:,:3] = ir_rvec
    R3x3,J = cv2.Rodrigues(ir_rvec)
    # extrinsic = forward_kinematic.Homo_matrix(ir_rvec[0],ir_tvec[0])[:3,:]
    # R3x3 = R3x3.transpose()
    # ir_tvec = -R3x3.dot(ir_tvec)
    extrinsic[:,:3] = R3x3
    extrinsic[:,3] = ir_tvec.transpose()[0]
    
    # print("pos_2d", pos_2d[0], pos_2d[1])
    # print(pos_3d_cam[0], pos_3d_cam[1])
    print extrinsic
    # np.save("extrinsic.npy",extrinsic)
    # np.save("extrinsic_1.npy",extrinsic)

    
    # rate = rospy.Rate(5)
    # while not rospy.is_shutdown():
    #     pos_3d = np.array(pos)
    #     print(pos_3d)
    #     pos_2d =  intrinsic_matrix.dot(pos_3d.transpose())
    #     us = pos_2d[0]/pos_2d[2]
    #     vs = pos_2d[1]/pos_2d[2]
    #     print(us.astype(int),vs)

    #     rate.sleep()
    

    # home_arm(pub)
    



if __name__ == "__main__":
    main()