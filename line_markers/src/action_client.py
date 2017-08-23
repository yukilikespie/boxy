#!/usr/bin/env python
import rospy
import actionlib
from giskard_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import *
from std_msgs.msg import *

cmd = WholeBodyCommand()
marker_points = []
header = Header()
input_points = []


def create_goal(normal, input_point):
    global cmd
    cmd.type = 0

    header.frame_id = "base_link"
    cmd.right_ee.goal_pose.header = header
    cmd.right_ee.type = 1

    cmd.right_ee.goal_pose.pose.orientation.w = 1.0

    # cmd.right_ee.goal_pose.pose.orientation.x = normal.x
    # cmd.right_ee.goal_pose.pose.orientation.y = normal.y
    # cmd.right_ee.goal_pose.pose.orientation.z = normal.z

    cmd.right_ee.goal_pose.pose.orientation.x = 0.0
    cmd.right_ee.goal_pose.pose.orientation.y = -0.4
    cmd.right_ee.goal_pose.pose.orientation.z = 4.0 + 0.1

    #print input_point
    p = Point()

    #p.x = input_point.x
    #p.y = input_point.y
    #p.z = input_point.z

   # p.x = 1.2 + 0.36
    #p.y = -1.0 + 0.25
    #p.z = 0.0 + 0.16
    #
    p.x = 1.0
    p.y = 0.0
    p.z = 1.2

    cmd.right_ee.goal_pose.pose.position = p

    goal = WholeBodyGoal(command=cmd)
    #goal.header = header
    #goal.goal = cmd
    #rospy.loginfo(goal)
    return goal


def action_client():
    client = actionlib.SimpleActionClient("/controller_action_server/move", WholeBodyAction)

    rospy.loginfo("Waiting for action server to start.")
    client.wait_for_server()
    rospy.loginfo("Action server started, sending goal.")

    for input_point in marker_points:
        normal = Point()

        goal = create_goal(normal, input_point)
        print goal

        client.send_goal(goal)
        client.wait_for_result()

        if client.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo("Made it!")
        else:
            rospy.loginfo("Failed.")

    #return client.get_result()


def callback(data):
    global header, marker_points
    header = data.header

    if data.type == Marker.POINTS:
        marker_points.extend(data.points)
    #print marker_points
    #elif data.type == Marker.ARROW:


def listener():
    rospy.Subscriber("visualization_marker", Marker, callback)
    #rospy.spin()


if __name__ == '__main__':
    rospy.init_node("action_client", anonymous=True)
    listener()

    try:
        action_client()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion.")
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
