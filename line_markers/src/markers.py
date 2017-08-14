#!/usr/bin/env python
import rospy
from messages.msg import *
from visualization_msgs.msg import *
from geometry_msgs.msg import *
from std_msgs.msg import *

input_points = []
input_normal = []
header = Header()


def callback(data):
    global header, input_points, input_normal
    header = data.header

    for data_point in data.line.points:
        input_points.append(data_point)

    input_normal.append(data.normal)


def listener():
    rospy.Subscriber("line_points", Line, callback)
    #rospy.spin()


def markers():
    pub = rospy.Publisher("visualization_marker", Marker, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        marker_points = Marker()
        marker_lines = Marker()
        marker_arrows = Marker()

        marker_points.header.frame_id = marker_lines.header.frame_id = marker_arrows.header.frame_id = header.frame_id
        marker_points.header.stamp = marker_lines.header.stamp = marker_arrows.header.stamp = header.stamp
        marker_points.ns = marker_lines.ns = marker_arrows.ns = "points"

        marker_points.id = 0
        marker_lines.id = 1
        marker_arrows.id = 2

        marker_points.pose.orientation.w = marker_lines.pose.orientation.w = marker_arrows.pose.orientation.w = 1.0
        marker_points.action = marker_lines.action = marker_arrows.action = Marker.ADD

        marker_points.type = Marker.POINTS
        marker_lines.type = Marker.LINE_STRIP
        marker_arrows.type = Marker.ARROW

        marker_points.scale.x = 0.15
        marker_points.scale.y = 0.15

        marker_lines.scale.x = 0.1

        marker_arrows.scale.x = 0.7
        marker_arrows.scale.y = 0.05
        marker_arrows.scale.z = 0.05

        marker_points.color.g = 1.0
        marker_points.color.a = 1.0

        marker_lines.color.b = 1.0
        marker_lines.color.a = 1.0

        marker_arrows.color.r = 1.0
        marker_arrows.color.b = 0.5
        marker_arrows.color.a = 1.0

        marker_points.lifetime = marker_lines.lifetime = marker_arrows.lifetime = rospy.Duration()

        for normal in input_normal:
            marker_arrows.pose.orientation.x = normal.x
            marker_arrows.pose.orientation.y = normal.y
            marker_arrows.pose.orientation.z = normal.z

        for input_point in input_points:
            p = Point()
            p.x = input_point.x
            p.y = input_point.y
            p.z = input_point.z

            marker_points.points.append(p)
            marker_lines.points.append(p)

            marker_arrows.pose.position = p
            marker_arrows.points.append(p)
            marker_arrows.id = marker_arrows.id + 1

        pub.publish(marker_points)
        pub.publish(marker_lines)
        pub.publish(marker_arrows)

        #rospy.loginfo(marker_points)
        #rospy.loginfo(marker_lines)
        #rospy.loginfo(marker_arrows)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node("line_marker", anonymous=True)

    listener()
    markers()
