#!/usr/bin/env python
import rospy
import random
from messages.msg._Points import *


def talker():
    pub = rospy.Publisher('line_points', Points, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)

    msg = Points()
    while not rospy.is_shutdown():
        msg.points = [12.00, random.uniform(10.00, 200.00), random.uniform(10.00, 200.00)]
        msg.normal = [0.0, 0.0, 1.0]

        rospy.loginfo(msg)
        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
