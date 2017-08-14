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
    i = 0.0
    j = 0.0
    while not rospy.is_shutdown():
        msg.header.frame_id = "/my_frame"
        msg.header.stamp = rospy.Time.now()

        p_start = Point32()
        p_start.x = 0.0
        p_start.y = i
        p_start.z = j
        msg.line.points.append(p_start)

        p_end = Point32()
        p_end.x = 0.0
        p_end.y = i + 2.0
        p_end.z = j
        msg.line.points.append(p_end)

        #i = i + random.uniform(2.0, 7.00)
        j = j + 0.5

        n = Point32()
        n.x = 0.0
        n.y = random.uniform(-0.2, 0.00)
        n.z = 0.0 #random.uniform(0.00, 5.00)
        msg.normal = n

        #rospy.loginfo(msg)
        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
