#!/usr/bin/env python
import rospy
import actionlib
from giskard_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import *
from std_msgs.msg import *

command = WholeBodyCommand()
marker_points = Point()
header = Header()
input_points = []
input_normal = []

start_point = Point32(1.0, -0.4, 1.3)
start_normal = Point32(0.0, 1.0, 0.0)
aux = 0


def create_goal():
    global input_points, input_normal, aux, start_point, start_normal

    command.type = 0
    header.frame_id = "base_link"

    command.right_ee.goal_pose.header = header
    command.right_ee.type = 1
    command.right_ee.goal_pose.pose.orientation.w = 1.0

    if len(input_points) >= 3:
        command.right_ee.goal_pose.pose.orientation.x = round(input_normal[aux].x, 2)
        command.right_ee.goal_pose.pose.orientation.y = round(input_normal[aux].y, 2)
        command.right_ee.goal_pose.pose.orientation.z = round(input_normal[aux].z, 2)

        command.right_ee.goal_pose.pose.position.x = round(input_points[aux].x, 2)
        command.right_ee.goal_pose.pose.position.y = round(input_points[aux].y, 2)
        command.right_ee.goal_pose.pose.position.z = round(input_points[aux].z, 2)

        aux += 1
    else:
        command.right_ee.goal_pose.pose.position = start_point

        command.right_ee.goal_pose.pose.orientation.x = start_normal.x
        command.right_ee.goal_pose.pose.orientation.y = start_normal.y
        command.right_ee.goal_pose.pose.orientation.z = start_normal.z

    goal = WholeBodyGoal(command=command)
    return goal


def action_client():
    client = actionlib.SimpleActionClient("/controller_action_server/move", WholeBodyAction)

    rospy.loginfo("Waiting for action server to start.")
    client.wait_for_server()
    rospy.loginfo("Action server started, sending goal.")

    goal = create_goal()
    rospy.loginfo(goal.command.right_ee.goal_pose.pose)

    client.send_goal(goal)
    finished_before_timeout = client.wait_for_result(rospy.Duration(30))

    if finished_before_timeout:
        state = client.get_state()
        rospy.loginfo("Action finished:" + str(state))
    else:
        rospy.loginfo("Action did not finish before the timeout.")


def callback(data):
    global header, input_points, input_normal

    if data.ns == "points":
        header = data.header
        input_points.append(data.pose.position)
    elif data.ns == "normal":
        input_normal.append(data.pose.orientation)


def listener():
    rospy.Subscriber("visualization_marker", Marker, callback)


if __name__ == '__main__':
    rospy.init_node("action_client", anonymous=True)

    while not rospy.is_shutdown():
        listener()

        try:
            action_client()
        except rospy.ROSInterruptException:
            print("Program interrupted before completion.")
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
