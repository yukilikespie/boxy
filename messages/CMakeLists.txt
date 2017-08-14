cmake_minimum_required(VERSION 2.8.3)
project(messages)

find_package(catkin REQUIRED COMPONENTS
	roscpp 
	rospy 
	geometry_msgs
	std_msgs
	message_generation
)

add_message_files(
	DIRECTORY msg
	FILES Line.msg
)

generate_messages(
	DEPENDENCIES std_msgs geometry_msgs
)	

catkin_package(
	CATKIN_DEPENDS message_runtime std_msgs geometry_msgs
)

include_directories(
	INCLUDE ${catkin_INCLUDE_DIRS}
)
