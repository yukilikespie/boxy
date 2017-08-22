#!/usr/bin/env python
import rospy
import actionlib
from markers import *
from giskard_msgs.msg import *
from geometry_msgs.msg import *
from std_msgs.msg import *

cmd = WholeBodyCommand()


def create_goal():
    global cmd
    cmd.type = 0

    header.frame_id = "base_footprint"
    cmd.right_ee.goal_pose.header = header
    cmd.right_ee.type = 1

    cmd.right_ee.goal_pose.pose.orientation.w = 1.0

    for normal in input_normal:
        cmd.right_ee.goal_pose.pose.orientation.x = normal.x
        cmd.right_ee.goal_pose.pose.orientation.y = normal.y
        cmd.right_ee.goal_pose.pose.orientation.z = normal.z

    for input_point in input_points:
        print input_point
        p = Point()

        p.x = input_point.x
        p.y = input_point.y
        p.z = input_point.z
        cmd.right_ee.goal_pose.pose.position = p

    goal = WholeBodyGoal(command=cmd)
    #goal.header = header
    #goal.goal = cmd
    rospy.loginfo(goal)
    return goal


def action_client():
    client = actionlib.SimpleActionClient("/controller_action_server/move", WholeBodyAction)

    rospy.loginfo("Waiting for action server to start.")
    client.wait_for_server()
    rospy.loginfo("Action server started, sending goal.")

    goal = create_goal()
    client.send_goal(goal)
    client.wait_for_result()

    return client.get_result()


if __name__ == '__main__':

    try:
        rospy.init_node('action_client')
        result = action_client()
        #rospy.loginfo(result)
    except rospy.ROSInterruptException:
        print("Program interrupted before completion.")
