#!/usr/bin/env python
import rospy
import random
from messages.msg._Points import *


def talker():
    pub = rospy.Publisher('line_points', Points, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)

    msg = Points()
    i = 0.00
    while not rospy.is_shutdown():
        msg.points = [1.00,  random.uniform(0.00, 5.00), 1.00]

        #msg.points = [0.0, i, 0.00]
        #i = i + random.uniform(0.00, 1.00)


        msg.normal = [0.0, random.uniform(0.00, 5.00), random.uniform(0.00, 5.00)]

        rospy.loginfo(msg)
        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
