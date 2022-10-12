#!/usr/bin/env phython

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int64
import sys

import numpy as np
import cv2
from cv_bridge import CvBridge

class MinimalCoordinatePublisher(Node):

	def __init__(self):
		super().__init__('minimal_coordinate_publisher')
		self.get_logger().info("Ball coordinate publisher has started!!")
		self.coor_publisher_ = self.create_publisher(Int64, '/turtlebot3/ball_pose', 10)

	def send_ball_coordinates(self, x_pose, y_pose):
		self.msg = Int64()
		self.msg = x_pose
		self.msg = y_pose
		self.coor_publisher_.publish(self.msg)

		


class MinimalVideoSubscriber(Node):

	def __init__(self):		
		#Creates the node.
		super().__init__('minimal_video_subscriber')
		self.get_logger().info("Ball detector has been started!!")

		#Set Parameters
		self.declare_parameter('show_image_bool', True)
		self.declare_parameter('window_name', "Ball Detector")

		#Determine Window Showing Based on Input
		self._display_image = bool(self.get_parameter('show_image_bool').value)

		#Declare some variables
		self._titleOriginal = self.get_parameter('window_name').value # Image Window Title	
		if(self._display_image):
		#Set Up Image Viewing
			cv2.namedWindow(self._titleOriginal, cv2.WINDOW_AUTOSIZE ) # Viewing Window
			cv2.moveWindow(self._titleOriginal, 50, 50) # Viewing Window Original Location
	
		#Declare that the minimal_video_subscriber node is subcribing to the /camera/image/compressed topic.
		self._video_subscriber = self.create_subscription(
				CompressedImage,
				'/camera/image/compressed',
				self._image_callback,
				1)
		self._video_subscriber # Prevents unused variable warning.

	def _image_callback(self, CompressedImage):	
		#The "CompressedImage" is transformed to a color image in BGR space and is store in "_imgBGR"
		self._imgBGR = CvBridge().compressed_imgmsg_to_cv2(CompressedImage, "bgr8")
		if(self._display_image):
			#Display the image in a window
			self.show_image(self._imgBGR)
				

	def get_image(self):
		return self._imgBGR

	def show_image(self, img):
		cv2.imshow(self._titleOriginal, img)
		#Cause a slight delay so image is displayed
		self._user_input=cv2.waitKey(10) #Use OpenCV keystroke grabber for delay.

	def process_img(self, img):
		self.gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		self.blur_frame = cv2.GaussianBlur(self.gray_frame, (15, 15), 1)
		self.blur_frame2 = cv2.medianBlur(self.blur_frame, 7)
		return self.blur_frame2
	
	def get_circle_ls(self, s_frame):
		self.circle_ls = cv2.HoughCircles(s_frame, cv2.HOUGH_GRADIENT, 0.7, 150, param1=100, param2=30, minRadius=50, maxRadius=0)
		return self.circle_ls

	def get_user_input(self):
		return self._user_input


def main():

	print("Beginning image processing")

	def calc_dist(x1,y1,x2,y2):
		dist = pow((x1 - x2), 2) + pow((y1 - y2), 2)
		return dist

	rclpy.init() #init routine needed fros2 run raspicam2 raspicam2_node ros-args params-file `ros2 pkg prefix raspicam2`/share/raspicam2/cfg/params.yamlor ROS2.
	video_subscriber = MinimalVideoSubscriber() #Create class object to be used.
	coor_publisher = MinimalCoordinatePublisher()

	while rclpy.ok():
		rclpy.spin_once(video_subscriber) # Trigger callback processing.
		if(True):
			
			main_frame = video_subscriber.get_image()
			edit_frame = video_subscriber.process_img(main_frame)
			circle_ls = video_subscriber.get_circle_ls(edit_frame)
			
			if circle_ls is not None:
				circle_ls = np.uint16(np.around(circle_ls))
				main_circle = None
				prev_circle = None
				#Detected circle position update
				for i in circle_ls[0,:]:
					if main_circle is None:
						main_circle = i
					if prev_circle is not None:
						if calc_dist(main_circle[0], main_circle[1], prev_circle[0], prev_circle[1]) <= calc_dist(i[0], i[1],prev_circle[0], prev_circle[1]):
							main_circle = i
					cv2.circle(main_frame, (main_circle[0], main_circle[1]), 1, (0,100,100), 3)
					cv2.circle(main_frame, (main_circle[0], main_circle[1]), main_circle[2], (255,0,255), 3)
					txt_mark = "x: " + str(main_circle[0]) + " y: " + str(main_circle[1]) 
					cv2.putText(main_frame, txt_mark, org=(main_circle[0], main_circle[1]),fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5 ,color=(102, 255, 51), thickness=2, lineType=cv2.LINE_AA)
					print("Ball Position: ", main_circle[0], main_circle[1])
					coor_publisher.send_ball_coordinates(int(main_circle[0]), int(main_circle[1]))
					prev_circle = main_circle
			else:
				coor_publisher.send_ball_coordinates(10000.0, 10000.0)

			
			video_subscriber.show_image(video_subscriber.get_image())		
			if video_subscriber.get_user_input() == ord('q'):
				cv2.destroyAllWindows()
				break

	#Clean up and shutdown.
	video_subscriber.destroy_node()  
	rclpy.shutdown()


if __name__ == '__main__':
	main()