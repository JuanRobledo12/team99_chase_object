import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
import sys
from random import randint
import time


class AngleTestPublisher(Node):
    
    def __init__(self):
        super().__init__('angle_test_publisher')
        self.get_logger().info("Test Publisher Started!!")
        self.angle_pub = self.create_publisher(Int64, '/lab3/pixel_pos', 5)
    
    def publish_random_pixels(self):
        self.msg = Int64()
        self.msg.data = randint(0, 320)
        self.angle_pub.publish(self.msg)

def main():
    rclpy.init()
    pixel_pub = AngleTestPublisher()

    while rclpy.ok:
        pixel_pub.publish_random_pixels()
        time.sleep(3)
    rclpy.shutdown()

if __name__ == '__main__':
	main()
    
