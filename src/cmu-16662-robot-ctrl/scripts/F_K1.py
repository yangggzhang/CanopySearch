import numpy as np
from math import *
from numpy.linalg import inv
# import vrep_utils as vu
from urdf_parser_py.urdf import URDF

file_name = "/home/zy/Documents/RobotAutonomy/catkin_ws/src/cmu-16662-robot-ctrl/locobot_description_v3.urdf"
robot = URDF.from_xml_file(file_name)
chains = robot.get_chain('arm_base_link', 'gripper_link',links =False)

class FK:
    def __init__(self,initial_joint_values,initial_joint_poses,a_cuboid_pos,a_cuboid_orient):
        self.H = np.zeros((5,4,4))
        self.u = np.zeros((5,3))

        # self.H[0] = self.Homo_matrix([0.0, 0.0, 0.0], initial_joint_poses[0])
        self.H[0] = self.Homo_matrix([0.0, 0.0, 0.0], [-8.96024853e-02, 3.87495442e-04, 1.59000054e-01])
        axis_xyz = robot.joint_map[chains[0]].axis
        self.u[0] = np.array(axis_xyz)

        for i in range(1,5):
          xyz = robot.joint_map[chains[i]].origin.xyz
          # print "xyz",xyz
          self.H[i] = self.Homo_matrix([0.0, 0.0, 0.0], xyz)
          axis_xyz = robot.joint_map[chains[i]].axis
          self.u[i] = np.array(axis_xyz)

        # print"Hs",self.H
        self.linkposes = self.get_link_pose(initial_joint_values[0:5])
        # print "linkposes",self.linkposes
        self.init_bb_trans = np.zeros((7,4,4))
        for i in range(7):
            bb_origin_trans = self.Homo_matrix(a_cuboid_orient[i],a_cuboid_pos[i])
            # print "bb_origin_trans",bb_origin_trans
            if i < 5:
                self.init_bb_trans[i] = np.matmul(np.linalg.inv(self.linkposes[i]),bb_origin_trans)
            else:
                self.init_bb_trans[i] = np.matmul(np.linalg.inv(self.linkposes[4]),bb_origin_trans)

    def Homo_matrix(self,rpy,xyz):
        M_r = np.array([[1,0,0,0],[0,np.cos(rpy[0]),-np.sin(rpy[0]),0],[0,np.sin(rpy[0]),np.cos(rpy[0]),0],[0,0,0,1]])
        M_p = np.array([[np.cos(rpy[1]),0,np.sin(rpy[1]),0],[0,1,0,0],[-np.sin(rpy[1]),0,np.cos(rpy[1]),0],[0,0,0,1]])
        M_y = np.array([[np.cos(rpy[2]),-np.sin(rpy[2]),0,0],[np.sin(rpy[2]),np.cos(rpy[2]),0,0],[0,0,1,0],[0,0,0,1]])
        Hmatrix = np.matmul(M_r,M_p)
        Hmatrix = np.matmul(Hmatrix,M_y)
        Hmatrix[0,3] = xyz[0]
        Hmatrix[1,3] = xyz[1]
        Hmatrix[2,3] = xyz[2]
        return Hmatrix

    def Angle_to_Matrix(self,ui,theta):
        Rmatrix = np.array([[ui[0]**2*(1-cos(theta))+cos(theta),ui[0]*ui[1]*(1-cos(theta))-ui[2]*sin(theta),ui[1]*sin(theta)+ui[0]*ui[2]*(1-cos(theta)),0],
                        [ui[2]*sin(theta)+ui[1]*ui[0]*(1-cos(theta)),(1-cos(theta))*ui[1]**2+cos(theta),ui[1]*ui[0]*(1-cos(theta))-ui[0]*sin(theta),0],
                        [ui[2]*ui[0]*(1-cos(theta))-ui[1]*sin(theta),ui[0]*sin(theta)+ui[2]*ui[1]*(1-cos(theta)),(1-cos(theta))*ui[2]**2+cos(theta),0],
                        [0,0,0,1]])
        return Rmatrix

    def get_link_pose(self,joint_angles):
        HT = np.zeros((5,4,4))
        R = np.zeros((5,4,4))
        # joint_angles = np.array(joint_angles)
        # print "joint_angles.shape",joint_angles.shape
        for i in range(5):
          R[i] = self.Angle_to_Matrix(self.u[i],joint_angles[i])

        HT[0] = np.dot(self.H[0],R[0])

        for i in range(1,5):
          HT[i] = np.dot(HT[i-1],self.H[i])
          HT[i] = np.dot(HT[i],R[i])

        return HT

    def get_bdbox_pose(self,joint_angles):
        bb_pose = np.zeros((7,4,4))
        self.linkposes = self.get_link_pose(joint_angles[0:5])
        for i in range(7):
            if i < 5:
                bb_pose[i] = np.matmul(self.linkposes[i],self.init_bb_trans[i])
            else:
                bb_pose[i] = np.matmul(self.linkposes[4],self.init_bb_trans[i])
        return bb_pose