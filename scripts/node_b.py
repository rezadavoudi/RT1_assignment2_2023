#!/usr/bin/env python3

import rospy
from assignment_2_2023.msg import Vel
from assignment_2_2023.srv import Input, InputResponse

# Initialize variables for the last desired x and y positions
last_x = 0
last_y = 0

# Initialize the ROS node
rospy.init_node('last_target_service')
rospy.loginfo("Last target node initialized")

# Callback function for the service
def handle_input_request(_):
    global last_x, last_y
    # Create a response message
    response = InputResponse()
    # Update the last x and y positions from parameters
    last_x = rospy.get_param('/des_pos_x')
    last_y = rospy.get_param('/des_pos_y')
    # Set the x and y inputs in the response
    response.input_x = last_x
    response.input_y = last_y

    # Return the response
    return response

# Setup the service
rospy.Service('input', Input, handle_input_request)

# Keep the node running
if __name__ == "__main__":
    rospy.spin()
