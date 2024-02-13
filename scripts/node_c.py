#!/usr/bin/env python3

import rospy
import math
from assignment_2_2023.msg import Vel
from assignment_2_2023.srv import Ave_pos_vel, Ave_pos_velResponse

# Initialize global variables for the average velocity and distance
average_velocity_x = 0
calculated_distance = 0

def update_distance_and_velocity(msg):
    global average_velocity_x, calculated_distance

    # Retrieve desired x and y positions and velocity window size from the parameter server
    desired_pos_x = rospy.get_param('/des_pos_x', 0)
    desired_pos_y = rospy.get_param('/des_pos_y', 0)
    velocity_window = rospy.get_param('/window_size', 1)

    # Extract actual x and y positions from the message
    actual_pos_x = msg.pos_x
    actual_pos_y = msg.pos_y

    # Calculate distance between desired and actual positions
    desired_coords = [desired_pos_x, desired_pos_y]
    actual_coords = [actual_pos_x, actual_pos_y]
    calculated_distance = math.dist(desired_coords, actual_coords)

    # Calculate the average velocity
    if isinstance(msg.vel_x, list) and len(msg.vel_x) > 0:
        velocity_data = msg.vel_x[-velocity_window:]
    else:
        velocity_data = [msg.vel_x]

    average_velocity_x = sum(velocity_data) / min(len(velocity_data), velocity_window)

    # Log the calculated distance and average velocity
    rospy.loginfo(f"Calculated Distance: {calculated_distance}, Average Velocity X: {average_velocity_x}")

def service_callback(request):
    global average_velocity_x, calculated_distance
    # Log receiving service request
    rospy.loginfo("Received service request for distance and average velocity.")
    return Ave_pos_velResponse(calculated_distance, average_velocity_x)

def initialize_node():
    rospy.init_node('info_service', anonymous=True)
    rospy.loginfo("Info service node initialized")

    rospy.Service("info_service", Ave_pos_vel, service_callback)
    rospy.Subscriber("/pos_vel", Vel, update_distance_and_velocity)

    rospy.spin()

if __name__ == "__main__":
    initialize_node()
