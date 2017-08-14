#!/usr/bin/env python
import rospy
import random
from messages.msg import *
from geometry_msgs.msg import *
from std_msgs.msg import *


def talker():
    pub = rospy.Publisher('line_points', Line, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)

    msg = Line()
    while not rospy.is_shutdown():
        msg.header.frame_id = "/my_frame"
        msg.header.stamp = rospy.Time.now()

        p = Point32()
        p.x = 0.0
        p.y = random.uniform(0.00, 5.00)
        p.z = 0.0
        msg.line.points.append(p)

        p.x = 0.0
        p.y = random.uniform(0.00, 5.00)
        p.z = 0.0
        msg.line.points.append(p)

        n = Point32()
        n.x = 0.0
        n.y = random.uniform(0.00, 5.00)
        n.z = random.uniform(0.00, 5.00)
        msg.normal = n

        #rospy.loginfo(msg)
        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
