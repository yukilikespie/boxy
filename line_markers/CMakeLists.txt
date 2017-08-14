cmake_minimum_required(VERSION 2.8.3)
project(line_markers)

find_package(catkin REQUIRED COMPONENTS
	roscpp 
	rospy 
	std_msgs
	message_generation
	messages
	visualization_msgs
	geometry_msgs
)

#add_message_files(
#	FILES
#	Points.msg
#)

#generate_messages(
#	DEPENDENCIES
#	std_msgs
#)	

catkin_package(
	CATKIN_DEPENDS rospy std_msgs messages message_runtime visualization_msgs geometry_msgs
)


 
include_directories(
	include ${catkin_INCLUDE_DIRS}
)

#rosbuild_add_executable(line_markers src/line_markers.py)

catkin_package()
