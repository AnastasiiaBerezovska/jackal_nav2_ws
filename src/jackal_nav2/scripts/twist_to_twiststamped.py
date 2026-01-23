#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class TwistToTwistStamped(Node): # this called node literally 
    def __init__(self):
        super().__init__('twist_to_twiststamped')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel_nav',
            #   '/cmd_vel_smoothed',
            self.twist_callback,
            10)
        self.publisher = self.create_publisher( # change later to /lonebot/cmd_vel
            TwistStamped,
             "/lonebot/platform/cmd_vel",
            # '/lonebot/joy_teleop/cmd_vel',
            # '/lonebot/bt_teleop/cmd_vel',
            # '/lonebot/cmd_vel',
            10)
        self.get_logger().info('Twist to TwistStamped converter started!')

    def twist_callback(self, msg):
        stamped_msg = TwistStamped()
        stamped_msg.header.stamp = self.get_clock().now().to_msg()
        stamped_msg.header.frame_id = 'lonebot/base_link'
        stamped_msg.twist = msg
        self.publisher.publish(stamped_msg)

def main(args=None):
    rclpy.init(args=args)
    node = TwistToTwistStamped()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()