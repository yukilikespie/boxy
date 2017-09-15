#!/usr/bin/env python

import rospy
from messages.msg import *
from giskard_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import *
from std_msgs.msg import *

input_points = []
input_normal = []
header = Header()

i = -3
step = 3
aux = 0

point_id = 0
line_id = 1
normal_id = 2

start_point = Point32(1.0, -0.4, 1.3)
start_normal = Point32(0.0, 1.0, 0.0)


def topic_listener():
    rospy.init_node("markers", anonymous=True)
    rospy.Subscriber("line_points", Line, callback)
    #rospy.spin()


def callback(msg_data):
    global header, input_points, input_normal

    header = msg_data.header
    input_points.append(msg_data.line.points[-1])
    input_normal.append(msg_data.normal)


def point_coordinates():
    global input_points, i, start_point

    if len(input_points) >= 3:
        return input_points[i]
    else:
        return start_point


def normal_coordinates():
    global input_normal, i, start_normal

    if len(input_normal) >= 3:
        return input_normal[i]
    else:
        return start_normal


def line_coordinates_start():
    global input_points, i, start_point

    if len(input_points) >= 3:
        return input_points[i-1]
    else:
        return start_point


def additional_points():
    global input_points, i, step, aux, start_point
    p = Point32()

    if len(input_points) >= 3:
        inc = abs(input_points[i].y - input_points[i+1].y) / step
        aux += inc

        if input_points[i].y < input_points[i+1].y:
            p.x = input_points[i].x
            p.y = input_points[i].y + aux
            p.z = input_points[i].z
            return p
        else:
            p.x = input_points[i].x
            p.y = input_points[i].y - aux
            p.z = input_points[i].z
            return p
    else:
        return start_point


def markers():
    global i, aux, point_id, line_id, normal_id, header

    pub = rospy.Publisher("visualization_marker", Marker, queue_size=10)
    rate = rospy.Rate(1)
    frame_id = 'base_link'

    while not rospy.is_shutdown():
        p = point_coordinates()

        marker_points = Marker()
        marker_lines = Marker()
        marker_normal = Marker()

        if header.frame_id == '':
            marker_points.header.frame_id = marker_lines.header.frame_id = marker_normal.header.frame_id = frame_id
        else:
            marker_points.header.frame_id = marker_lines.header.frame_id = marker_normal.header.frame_id = header.frame_id

        marker_points.header.stamp = marker_normal.header.stamp = marker_lines.header.stamp = rospy.Time.now()
        marker_points.lifetime = marker_lines.lifetime = marker_normal.lifetime = rospy.Duration()
        marker_points.action = marker_lines.action = marker_normal.action = Marker.ADD
        marker_points.pose.orientation.w = marker_lines.pose.orientation.w = marker_normal.pose.orientation.w = 1.0

        marker_points.type = Marker.SPHERE
        marker_lines.type = Marker.LINE_STRIP
        marker_normal.type = Marker.ARROW

        marker_points.scale.x = 0.05
        marker_points.scale.y = 0.05
        marker_points.scale.z = 0.05

        marker_lines.scale.x = 0.025
        marker_lines.scale.y = 0.025
        marker_lines.scale.z = 0.025

        marker_normal.scale.x = 0.25
        marker_normal.scale.y = 0.025
        marker_normal.scale.z = 0.025

        marker_lines.color.r = 0.0
        marker_lines.color.g = 1.0
        marker_lines.color.b = 0.5
        marker_lines.color.a = 1.0

        marker_points.color.b = 0.7
        marker_points.color.a = 1.0

        marker_normal.color.r = 1.0
        marker_normal.color.g = 1.0
        marker_normal.color.a = 1.0

        marker_points.ns = "points"
        marker_lines.ns = "line marker"
        marker_normal.ns = "normal"

        marker_points.id = point_id
        marker_lines.id = line_id
        marker_normal.id = normal_id

        marker_points.pose.position = marker_normal.pose.position = p
        marker_lines.points.append(line_coordinates_start())
        marker_lines.points.append(p)

        current_normal = normal_coordinates()
        marker_normal.pose.orientation.x = current_normal.x
        marker_normal.pose.orientation.y = current_normal.y
        marker_normal.pose.orientation.z = current_normal.z

        # PUBLISH SECTION
        pub.publish(marker_points)
        #print marker_points.pose.position
        point_id += 1

        pub.publish(marker_normal)
        normal_id += 1

        if point_id % 2 != 0:
            for k in range(0, step-1):
                pt = additional_points()
                marker_normal.id = normal_id
                marker_points.id = point_id

                marker_points.pose.position = pt
                marker_normal.pose.position = pt

                marker_lines.points.append(pt)

                pub.publish(marker_points)
                #print marker_points.pose.position
                pub.publish(marker_normal)

                point_id += 1
                normal_id += 1

        pub.publish(marker_points)
        pub.publish(marker_lines)

        aux = 0
        line_id += 1
        i += 1

        rate.sleep()

if __name__ == '__main__':
    topic_listener()
    markers()
