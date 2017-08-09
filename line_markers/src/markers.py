#!/usr/bin/env python
import rospy
from messages.msg._Points import *
from visualization_msgs.msg import *
from geometry_msgs.msg import Point
import tf
import math

input_points = []
input_normal = []


def callback(data):
    global input_points, input_normal
    input_points.append(data.points)
    input_normal.append(data.normal)

    #for i in range(0, 2):
     #   input_points = [1, i, i+1]

    print input_points


def listener():
    rospy.init_node('line_marker', anonymous=True)
    rospy.Subscriber("line_points", Points, callback)
    rospy.spin()


def markers():
    rospy.init_node("line_marker")
    pub = rospy.Publisher("visualization_marker", Marker, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        marker_points = Marker()
        marker_points.header.frame_id = "/my_frame"
        marker_points.header.stamp = rospy.Time.now()

        marker_points.ns = "points"
        marker_points.id = 0

        marker_points.pose.orientation.w = 1.0

        marker_points.type = Marker.POINTS
        marker_points.action = Marker.ADD

        # marker_points.scale.x = 1.0
        # marker_points.scale.y = 1.0
        # marker_points.scale.z = 1.0
        #
        # marker_points.color.r = 0.0
        # marker_points.color.g = 1.0
        # marker_points.color.b = 0.5
        # marker_points.color.a = 1.0
        #
        # p = Point
        # for i in range(0, 200):
        #     y = i
        #     z = i
        #     p.x = 0.5
        #     p.y = y
        #     p.z = z
        #     marker_points.points.append(p)
        #     #print marker_points

        marker_points.pose.position.x = 0
        marker_points.pose.position.y = 0
        marker_points.pose.position.z = 0

        marker_points.pose.orientation.x = 0.0
        marker_points.pose.orientation.y = 0.0
        marker_points.pose.orientation.z = 0.0
        marker_points.pose.orientation.w = 1.0

        marker_points.scale.x = 1.0
        marker_points.scale.y = 1.0
        marker_points.scale.z = 1.0

        marker_points.color.r = 0.0
        marker_points.color.g = 1.0
        marker_points.color.b = 0.0
        marker_points.color.a = 1.0

        marker_points.lifetime = rospy.Duration()

        for i in range(0, 100):
            y = 5*math.sin(i/100.00*2*math.pi)
            z = 5*math.cos(i/100.00*2*math.pi)

            p = Point()
            p.x = i - 50
            p.y = y
            p.z = z

            marker_points.points.append(p)
            p.z = p.z + 1.0

        pub.publish(marker_points)
        rospy.loginfo(marker_points)
        rate.sleep()


def wut():
    rospy.init_node("basic_shapes")
    r = rospy.Rate(1)
    marker_pub = rospy.Publisher("visualization_marker", Marker, queue_size=10)
    shape = Marker.CUBE

    while not rospy.is_shutdown():
        marker = Marker()
        marker.header.frame_id = "/my_frame"
        marker.header.stamp = rospy.Time.now()

        marker.ns = "basic_shapes"
        marker.id = 0

        marker.type = shape
        marker.action = Marker.ADD

        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0

        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0

        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker.lifetime = rospy.Duration()

        marker_pub.publish(marker)

        r.sleep()


if __name__ == '__main__':
    #listener()
    markers()

    #wut()
