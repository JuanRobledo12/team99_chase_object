from rclpy.qos import qos_profile_sensor_data, QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy
from sensor_msgs.msg import LaserScan
import rclpy

def chatter_callback(msg):
    #print("msg: ", msg)
    # # values at 0 degree
    print(msg.ranges[0])
    # # values at 90 degree
    # print(msg.ranges[360])
    # # values at 180 degree
    # print (msg.ranges[719])
 
def main():
    rclpy.init()
    qos_profile = QoSProfile(depth=10)
    qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
    qos_profile.durability = QoSDurabilityPolicy.VOLATILE
    node = rclpy.create_node('scan_listener')
    sub = node.create_subscription(LaserScan,'scan', chatter_callback, qos_profile)
    try:
        while True:
            rclpy.spin_once(node)
  
    except KeyboardInterrupt:
        pass
  
if __name__ == "__main__":
    print('Starting scan listener')
    main()
    print('done.')        