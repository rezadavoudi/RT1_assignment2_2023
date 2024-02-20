# RT1_assignment2_2023
# Reza DAVOUDI BENI (6115320)

## Overview
This assignment involves the development of a ROS-based system with three interconnected nodes. Each node performs specific tasks and communicates with others to achieve a common goal. The system utilizes topics, services, and action servers for inter-node communication.

## Nodes Description

### Node A

  - Accepts user input to set new goal positions.
  - Publishes position and velocity information to the `/pos_vel` topic.
  - Sends goal positions to `node B` through the `reaching_goal` action server.

### Node B

  - Provides a service to retrieve the last set desired x and y positions by `node A`.
  - Stores the last desired positions and responds to service requests from other nodes.

### Node C

  - Subscribes to the `/pos_vel` topic to receive position and velocity information.
  - Calculates the distance between the desired and actual positions.
  - Computes the average velocity along the x-axis.
  - Offers a service to other nodes to query the calculated distance and average velocity.


## Installation Instructions

1. Ensure you have ROS installed on your system.
2. Create a ROS workspace if not already present.
3. Clone this repository into the `src` directory of your ROS workspace.
4. Build the ROS packages using `catkin_make`.


