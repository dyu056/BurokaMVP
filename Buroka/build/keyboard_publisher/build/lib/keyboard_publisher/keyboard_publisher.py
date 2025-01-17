import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import sys
import termios
import tty

class KeyboardPublisher(Node):
    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(Int32, '/cmd', 10)
        self.get_logger().info("Publishing keyboard input (0-9). Press 'Ctrl+C' to exit.")

    def get_key(self):
        # Set terminal to raw mode to capture single key press
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        while rclpy.ok():
            key = self.get_key()  # Capture a single key press
            if key.isdigit() and 0 <= int(key) <= 9:  # Only accept digits 0-9
                msg = Int32()
                msg.data = int(key)
                self.publisher_.publish(msg)
                self.get_logger().info(f"Published: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardPublisher()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
