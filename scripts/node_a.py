#!/usr/bin/env python3

# Import necessary libraries
import rospy
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
import actionlib
from assignment_2_2023.msg import Vel, PlanningAction, PlanningGoal
from actionlib_msgs.msg import GoalStatus

# Initialize global variables for publisher and action client
pub_velocity = rospy.Publisher("/pos_vel", Vel, queue_size=1)
goal_client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)


# Function to publish position and velocity
def publish_position_and_velocity(msg):
    # Extract current position and velocity from the Odometry message
    current_position = msg.pose.pose.position
    current_velocity_linear = msg.twist.twist.linear
    current_velocity_angular = msg.twist.twist.angular

    # Create a new Vel message with the current position and velocity
    position_velocity_message = Vel()
    position_velocity_message.pos_x = current_position.x
    position_velocity_message.pos_y = current_position.y
    position_velocity_message.vel_x = current_velocity_linear.x
    position_velocity_message.vel_z = current_velocity_angular.z

    # Publish the Vel message
    pub_velocity.publish(position_velocity_message)


# Function to handle goal commands
def handle_goal_commands():
    goal_cancelled = True  # Flag to track if the current goal has been cancelled
    goal_client.wait_for_server()

    while not rospy.is_shutdown():
        # Subscribe to /odom topic and publish position and velocity
        rospy.Subscriber("/odom", Odometry, publish_position_and_velocity)
        # Get user command
        command = input("Press 'n' for setting a new goal or 'e' to exit: ")
        # Get current target position
        target_pos_x = rospy.get_param('/des_pos_x')
        target_pos_y = rospy.get_param('/des_pos_y')

        # Create a new goal with the current target position
        goal = PlanningGoal()
        goal.target_pose.pose.position.x = target_pos_x
        goal.target_pose.pose.position.y = target_pos_y
        rospy.loginfo(f"Current goal: target_x = {target_pos_x}, target_y = {target_pos_y}")

        if command == 'n':
            try:
                # Get new goal coordinates from user
                input_x = float(input("Enter the new x-coordinate: "))
                input_y = float(input("Enter the new y-coordinate: "))
            except ValueError:
                rospy.logwarn("Invalid input.")
                continue

            # Update target position parameters and the goal
            rospy.set_param('/des_pos_x', input_x)
            rospy.set_param('/des_pos_y', input_y)
            goal.target_pose.pose.position.x = input_x
            goal.target_pose.pose.position.y = input_y

            # Send the new goal to the action server
            goal_client.send_goal(goal)
            goal_cancelled = False

        elif command == 'e':
            if not goal_cancelled:
                # Cancel the current goal if there is one
                goal_cancelled = True
                goal_client.cancel_goal()
                rospy.loginfo("Current goal has been cancelled")
            else:
                rospy.loginfo("No active goal to cancel")
        else:
            rospy.logwarn("Invalid command. Please enter 'n' or 'e'.")

        rospy.loginfo(
            f"Last received goal: target_x = {goal.target_pose.pose.position.x}, target_y = {goal.target_pose.pose.position.y}")


def main():
    # Initialize the node
    rospy.init_node('set_target_client')
    handle_goal_commands()


if __name__ == '__main__':
    main()
