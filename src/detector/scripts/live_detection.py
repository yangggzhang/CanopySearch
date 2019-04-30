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

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("ros_image",Image)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
    self.approx = None
    self.detector = CanopyDetector()
    self.progress = False
    self.start_point = None
    self.target_point = None
  
  def project(self, x, y, z):
    P = [-0.26258097, -0.96485145,  0.01062577,  0.02905107, -0.0808903,  0.01103792, -0.99666189,  0.48671212, 0.96151339, -0.26256397, -0.08094547, 0.21650044]
    proj_x = P[0] * x + P[1] * y + P[2] * z + P[3]
    proj_y = P[4] * x + P[5] * y + P[6] * z + P[7]
    proj_z = P[8] * x + P[9] * y + P[10] * z + P[11]
    return proj_x, proj_y, proj_z
    
  def move_arm_client(self, x0, y0, z0, x1, y1, z1):
    rospy.wait_for_service('move_arm')
    try:
        move_ser = rospy.ServiceProxy('move_arm', MovePos)
        print("sending")
        resp = move_ser(x0, y0, z0, x1, y1, z1)
        return resp.reached
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

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

    if not self.progress:
      target = random.choice(targets)
      self.start_point = (points[0], points[1])
      self.target_point = (points[2], points[3])
      self.progress = self.move_arm_client()
    
    

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