#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from detection import CanopyDetector
import numpy as np
import random
from move_canopy.srv import MovePos
from move_canopy.msg import push
from move_canopy.msg import confirm

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("ros_image",Image)
    self.arm_pub = rospy.Publisher('push', push)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
    self.grab_sub = rospy.Subscriber("grab_status", confirm, self.confirm_callback)
    self.approx = None
    self.detector = CanopyDetector()
    self.grab_state = False # true finished
    self.start_point = None
    self.target_point = None
    self.RGB_start_point = None
    self.RGB_target_point = None
    self.z = 0.4435
    self.P = [614.357421875, 0.0, 310.2319641113281, 0.0, 0.0, 614.494140625, 244.32691955566406, 0.0, 0.0, 0.0, 1.0, 0.0]
    self.T = np.array([[-0.26258097, -0.96485145,  0.01062577,  0.02905107],
                       [-0.0808903,  0.01103792, -0.99666189,  0.48671212], 
                       [0.96151339, -0.26256397, -0.08094547, 0.21650044],
                       [0.0,0.0,0.0,1.0]])
  
  def confirm_callback(data):
    self.grab_state = data.confirm
  
  def project(self, x, y):
    A = np.array([[self.P[0], self.P[1], -x], 
                  [self.P[4], self.P[5], -y],
                  [self.P[8], self.P[9], -1]])
    B = np.array([[-self.P[3] - self.P[2]*self.z],
                  [-self.P[7] - self.P[6]*self.z],
                  [-self.P[11]- self.P[10]*self.z]]) 
    loc = np.matmul(np.linalg.inv(A), B)
    carmera_xyz = np.vstack((loc, [1]))
    proj_xyz = np.matmul(np.linalg.inv(self.T), carmera_xyz)    
    return proj_xyz[0], proj_xyz[1], proj_xyz[2]

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      self.detector.init_image(cv_image)
    except CvBridgeError as e:
      print(e)
      

    if self.approx is None:
        self.approx = self.detector.background()
        print("finish detect black board")
    cv2.drawContours(cv_image, self.approx, -1, (255,255,255), 3)

    apple, count = self.detector.apple()
    cv2.drawContours(cv_image, apple, -1, (255, 0, 0), 3)
    print(count)

    leaves, targets = self.detector.leaves()
    cv2.drawContours(cv_image, leaves, -1, ( 0, 255, 0), 3)

    if not self.grab_state:
      points = random.choice(targets)
      self.RGB_start_point = (points[0], points[1])
      self.RGB_target_point = (points[2], points[3])
      self.start_point = self.project(points[0], points[1])
      self.target_point = self.project(points[2], points[3])

      msg = push()
      msg.x0 = self.start_point[0]
      msg.y0 = self.start_point[1]
      msg.z0 = self.start_point[2]
      msg.x1 = self.target_point[0]
      msg.y1 = self.target_point[1]
      msg.z1 = self.target_point[2]
      self.arm_pub.publish(msg)

      print("Point 1", self.start_point)
      print("Point 2", self.target_point)
      
      # self.progress = self.move_arm_client(self.start_point[0], self.start_point[1], self.start_point[2],
      #                                      self.target_point[0],self.target_point[1],self.target_point[2])
    cv2.circle(cv_image,self.RGB_start_point, 10, (255,0,0), -1)
    cv2.circle(cv_image,self.RGB_target_point, 10, (255,0,0), -1)
    # print("Point 1", self.start_point)
    # print("Point 2", self.target_point)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)