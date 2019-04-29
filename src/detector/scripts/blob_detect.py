# Standard imports
import cv2
import numpy as np
from detection import CanopyDetector
 
# Read image
img = cv2.imread("/home/parallels/Documents/CanopySearch/data/2.png", cv2.IMREAD_COLOR)


detector = CanopyDetector(img)

approx = detector.background()
cv2.drawContours(img, approx, -1, (255,255,255), 3)
cv2.imshow("black_coutour", img)
cv2.waitKey(0)

apple = detector.apple()
cv2.drawContours(img, apple, -1, (255, 0, 0), 3)
cv2.imshow("apple", img)
cv2.waitKey(0)

leaves = detector.leaves()
cv2.drawContours(img, leaves, -1, ( 0, 255, 0), 3)
cv2.imshow("leaves", img)
cv2.waitKey(0)