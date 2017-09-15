#!/usr/bin/env python

import rospy
import std_msgs.msg
from geometry_msgs.msg import *
from messages.msg import *


def talker():
    pub = rospy.Publisher('line_points', Line, queue_size=10)
    rospy.init_node('point_publisher', anonymous=True)
    rate = rospy.Rate(1)

    msg = Line()
    a = 1

    p = Point32()
    p.x = 1.0
    p.y = -0.5
    p.z = 0.6

    while not rospy.is_shutdown():
        msg.header.frame_id = "base_link"
        msg.header.stamp = rospy.Time.now()

        if a % 2 == 0:
            p.x = 1.1
            p.y = -0.5
            #p.z = 0.5
        else:
            p.x = 1.1
            p.y += 0.4
            p.z += 0.10

        n = Point32()
        n.x = 0.0
        n.y = 1.0
        n.z = 0.0
        msg.normal = n

        a += 1

        if a > 4:
            msg.line.points.append(p)
            pub.publish(msg)
            rospy.loginfo(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
