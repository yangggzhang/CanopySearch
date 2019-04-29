import rospy
from move_canopy.srv import MovePos

def move_arm_client(x, y, z):
    rospy.wait_for_service('move_arm')
    try:
        move_ser = rospy.ServiceProxy('move_arm', MovePos)
        print("sending")
        resp = move_ser(x, y, z)
        return resp.reached
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    x = 1.0
    y = 1.0
    z = 1.0
    print "Requesting %s+%s+%s"%(x, y, z)
    print(move_arm_client(x, y, z))