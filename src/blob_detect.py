# Standard imports
import cv2
import numpy as np;
 
# Read image
img = cv2.imread("../data/2.png", cv2.IMREAD_COLOR)

cv2.imshow("test_image", img)
cv2.waitKey(0)

img_copy0 = img.copy()
img_copy1 = img.copy()
# to red image
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


lower_black = np.array([   0,   0,  0])
upper_black = np.array([ 180, 255, 50])

black_mask = cv2.inRange(hsv, lower_black, upper_black)

black_mask = cv2.dilate(black_mask,np.ones((5,5),np.uint8),iterations = 1)
black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))

black_img = cv2.bitwise_and(img, img, mask = black_mask)

black_imggray = cv2.cvtColor(black_img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(black_imggray,0,30,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# im2, contours, hierarchy = cv2.findContours(thresh,2,1)


#find the largest contour
largest_area = 0
black_cnt = []
for c in contours:
    if cv2.contourArea(c) > largest_area:
        largest_area = cv2.contourArea(c)
        black_cnt = c

eps_const = 0.05
epsilon = eps_const*cv2.arcLength(black_cnt,True)
approx = cv2.approxPolyDP(black_cnt,epsilon,True)

# cv2.drawContours(img_copy1, black_cnt, -1, (0,255,255), 3)
cv2.drawContours(img_copy0, [approx], -1, (255,255,255), 3)
cv2.imshow("black_coutour", img_copy0)
cv2.waitKey(0)


# cv2.imshow("OriginalImage",im)
 
# mask out red fruits

# Range for lower red
lower_red = np.array([0,120,70])
upper_red = np.array([10,255,255])
red_mask1 = cv2.inRange(hsv, lower_red, upper_red)
 
# Range for upper range
lower_red = np.array([170,120,70])
upper_red = np.array([180,255,255])
red_mask2 = cv2.inRange(hsv,lower_red,upper_red)
 
# Generating the final mask to detect red color
red_mask = red_mask1 + red_mask2

red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
 
#creating an inverted mask to segment out the cloth from the frame 
#Segmenting the cloth out of the frame using bitwise and with the inverted mask
red_img = cv2.bitwise_and(img,img,mask=red_mask)

imgray = cv2.cvtColor(red_img,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(imgray,0,125,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

filtered_countours = []
#filter countours based on size
for c in contours:
    if cv2.contourArea(c) >= 200:
        filtered_countours.append(c)

cv2.drawContours(img_copy0, filtered_countours, -1, (255,0,0), 3)
cv2.imshow("apples", img_copy0)
cv2.waitKey(0)

# mask out green leaves

sensitivity = 30

# Range for green
lower_green = np.array([ max(  0, 60 - sensitivity), 100,  50])
upper_green = np.array([ min(255, 60 + sensitivity), 255, 255])
green_mask = cv2.inRange(hsv, lower_green, upper_green)

green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
 
#creating an inverted mask to segment out the cloth from the frame 
#Segmenting the cloth out of the frame using bitwise and with the inverted mask
green_img = cv2.bitwise_and(img,img, mask = green_mask)

# cv2.imshow("coutours", green_img)
# cv2.waitKey(0)

green_imgray = cv2.cvtColor(green_img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(green_imgray,0,180,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

filtered_countours = []
#filter countours based on size
for c in contours:
    if cv2.contourArea(c) >= 200:
        filtered_countours.append(c)

cv2.drawContours(img_copy0, filtered_countours, -1, (0,255,0), 3)
cv2.imshow("leaves", img_copy0)
cv2.waitKey(0)
# Set up the detector with default parameters.
# detector = cv2.SimpleBlobDetector_create()
 
# # Detect blobs.
# keypoints = detector.detect(img)
 
# # Draw detected blobs as red circles.
# # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
# im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# # Show keypoints

# cv2.imshow("Keypoints", im_with_keypoints)
# cv2.waitKey(0)