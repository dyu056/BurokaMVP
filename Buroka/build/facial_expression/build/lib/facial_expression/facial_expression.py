import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import os
import cv2

class FacialExpressionPlayer(Node):

    def __init__(self):
        super().__init__('integer_subscriber')
        self.cmd_sub = self.create_subscription(Int32, '/cmd', self.cmd_callback, 10)
        self.img_pub = self.create_publisher(Image, '/video_player', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.i = 0

        self.folder_name = "0"
        self.folder_base_path = "/home/dyu056/Projects/Buroka/videos/"
        self.folder_path = self.folder_base_path + self.folder_name
        self.max_i = get_max_number(self.folder_path)
        self.bridge = CvBridge()

    def cmd_callback(self, msg):
        # While receiving cmd, change the folder to play the image
        self.get_logger().info(f'Received command: {msg.data}')
        self.folder_name = str(msg.data)
        self.folder_path = self.folder_base_path + self.folder_name
        self.max_i = get_max_number(self.folder_path)
        self.i = 0

    def timer_callback(self):
        img_path = self.folder_path + "/" + str(self.i) + ".jpg"
        # Read an image from file using OpenCV
        cv_image = cv2.imread(img_path)
        # Convert the OpenCV image (BGR) to ROS Image message (RGB)
        ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        self.get_logger().info(f'Publishing: {img_path}')
        # Publish the image message
        self.img_pub.publish(ros_image)

        if self.i == self.max_i:
            self.i = 0
        else:
            self.i += 1

def get_max_number(folder_path):
    max_number = -1
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.jpg') and file_name[:-4].isdigit():  # Check for .jpg and numeric names
            max_number = max(max_number, int(file_name[:-4]))
    return max_number

def main(args=None):
    rclpy.init(args=args)
    node = FacialExpressionPlayer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

