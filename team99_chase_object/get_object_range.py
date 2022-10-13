from rclpy.qos import qos_profile_sensor_data, QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int64
import rclpy
from rclpy.node import Node
import sys

class BallAngularPosition(Node):
    
  

    def __init__(self):
        super().__init__('ball_anglular_position')
        self.pose_sub = self.create_subscription(Int64, '/lab3/pixel_pos', self.get_ball_coordinates, 10)
        self.get_logger().info("Ball Location Subscriber Started!!")
        self.angle_pub = self.create_publisher(Int64, '/lab3/angular_pos', 5)
    
    def get_ball_coordinates(self, msg: Int64):   
        #print(msg)
        self.new_msg = Int64()
        #Convert pixel value of ballposx to angle values
        self.new_msg.data = int((msg.data * 62) / 320)
        print(self.new_msg)
        self.angle_pub.publish(self.new_msg)   
       
        
class BallLinearPosition(Node):

    def __init__(self):
        super().__init__('ball_linear_position')
        self.qos_profile = QoSProfile(depth=10)
        self.qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        self.qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        self.lidar_sub = self.create_subscription(LaserScan, '/scan', self.lidar_callback, self.qos_profile)
    
    def lidar_callback(msg):
        #print("msg: ", msg)
        # # values at 0 degree
        print(msg.ranges[0])
        # # values at 90 degree
        # print(msg.ranges[360])
        # # values at 180 degree
        # print (msg.ranges[719])
 
def main():
    rclpy.init()
    angular_pos = BallAngularPosition()
    linear_pos = BallLinearPosition()
    rclpy.spin(angular_pos)
    rclpy.shutdown()
  
if __name__ == '__main__':
    main()      