import rospy
from move_canopy.srv import MovePos

def move_arm_client(x0, y0, z0, x1, y1, z1):
    rospy.wait_for_service('move_arm')
    try:
        move_ser = rospy.ServiceProxy('move_arm', MovePos)
        print("sending")
        resp = move_ser(x0, y0, z0, x1, y1, z1)
        return resp.reached
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    x1 = 0.29882201
    y1 = 0.06916873
    z1 = 0.32085176
    x0 = 0.25532813
    y0 = -0.09754627
    z0 = 0.34498405
    print(move_arm_client(x0, y0, z0, x1, y1, z1))