# Standard imports
import cv2
import numpy as np

class CanopyDetector():
    def __init__(self):
        #
        self.frame = None
        self.hsv = None
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.apple_mask = None

    def init_image(self, frame):
        self.frame = frame
        self.hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    def background(self):
        lower_black = np.array([   0,   0,  0])
        upper_black = np.array([ 180, 255, 50])

        black_mask = cv2.inRange(self.hsv, lower_black, upper_black)

        black_mask = cv2.dilate(black_mask,np.ones((15,15),np.uint8),iterations = 1)
        black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))

        black_img = cv2.bitwise_and(self.frame, self.frame, mask = black_mask)

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
        
        self.x_min = approx[0][0][0]
        self.x_max = approx[0][0][0]
        self.y_min = approx[0][0][1]
        self.y_max = approx[0][0][1]
        for corner in approx:
            if corner[0][0] < self.x_min:
                self.x_min = corner[0][0]
            if corner[0][0] > self.x_max:
                self.x_max = corner[0][0]
            if corner[0][1] < self.y_min:
                self.y_min = corner[0][1]
            if corner[0][1] > self.y_max:
                self.y_max = corner[0][1]

        return [approx]
    
    def apple(self):
        count = 0
        # Range for lower red
        lower_red = np.array([0,120,70])
        upper_red = np.array([10,255,255])
        red_mask1 = cv2.inRange(self.hsv, lower_red, upper_red)
        
        # Range for upper range
        lower_red = np.array([170,120,70])
        upper_red = np.array([180,255,255])
        red_mask2 = cv2.inRange(self.hsv,lower_red,upper_red)
        
        # Generating the final mask to detect red color
        red_mask = red_mask1 + red_mask2

        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
        if self.apple_mask is None:
            self.apple_mask = red_mask
        else:
            self.apple_mask = cv2.bitwise_or(red_mask, self.apple_mask)
        
        #creating an inverted mask to segment out the cloth from the frame 
        #Segmenting the cloth out of the frame using bitwise and with the inverted mask
        red_img = cv2.bitwise_and(self.frame,self.frame,mask=self.apple_mask)

        imgray = cv2.cvtColor(red_img,cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(imgray,0,125,0)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        filtered_countours = []
        #filter countours based on size
        for c in contours:
            if cv2.contourArea(c) >= 200:
                M = cv2.moments(c)
                cx = M['m10']/M['m00']
                cy = M['m01']/M['m00']
                if cx >= self.x_min and cx <= self.x_max and cy >= self.y_min and cy <= self.y_max:
                    filtered_countours.append(c)
                    count = count + 1
                
        return filtered_countours, count

    def leaves(self):
        sensitivity = 30
        # Range for green
        lower_green = np.array([ max(  0, 60 - sensitivity), 100,  50])
        upper_green = np.array([ min(255, 60 + sensitivity), 255, 255])
        green_mask = cv2.inRange(self.hsv, lower_green, upper_green)

        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
        
        #creating an inverted mask to segment out the cloth from the frame 
        #Segmenting the cloth out of the frame using bitwise and with the inverted mask
        green_img = cv2.bitwise_and(self.frame, self.frame, mask = green_mask)

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
        
        return filtered_countours
