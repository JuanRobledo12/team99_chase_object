#!/usr/bin/env phython

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int64

class BallFollower(Node):

    def __init__(self):
        super().__init__('ball_follower')
        self.ang_pos_subscriber_ = self.create_subscription(Int64, '/lab3/angular_pos', self.get_ball_coordinates, 10)
        self.get_logger().info("Rotation control node started!!")
        self.vel_publisher = self.create_publisher(Twist, '/cmd_vel', 5)

    def get_ball_coordinates(self, msg: Int64, center = 31, speed_gain = 2):
        self.vel_msg = Twist()
        #self.get_logger().info(str(msg.linear.x))
        ballpos_x = msg.data
        if (ballpos_x >= center-5) and (ballpos_x <= center+5):
            self.get_logger().info('the ball is already in the center')
            self.vel_msg.angular.z = 0.0
            self.vel_publisher.publish(self.vel_msg) 
        elif (ballpos_x < center-5) or ((ballpos_x > center+5) and (ballpos_x <= 62)):
            speed = speed_gain * -(ballpos_x-center) / center
            self.get_logger().info('rotating...')
            self.vel_msg.angular.z = speed
            self.vel_publisher.publish(self.vel_msg)
        elif (ballpos_x >= 10000.0):
            self.get_logger().info("I'm lost, please help me!")
            self.vel_msg.angular.z = 0.0
            self.vel_publisher.publish(self.vel_msg)
        


def main():
    rclpy.init()
    pose_sub = BallFollower()
    rclpy.spin(pose_sub)
    rclpy.shutdown()

if __name__ == '__main__':
	main()
