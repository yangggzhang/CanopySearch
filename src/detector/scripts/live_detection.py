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

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("ros_image",Image)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
    self.approx = None
    self.detector = CanopyDetector()

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    if self.detector.frame is None:
      self.detector.init_image(cv_image)
      print("finish iniitalizaiton")

    if self.approx is None:
        self.approx = self.detector.background()
        print("finish detect black board")
    cv2.drawContours(cv_image, self.approx, -1, (255,255,255), 3)

    apple = self.detector.apple()
    cv2.drawContours(cv_image, apple, -1, (255, 0, 0), 3)

    leaves = self.detector.leaves()
    cv2.drawContours(cv_image, leaves, -1, ( 0, 255, 0), 3)

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