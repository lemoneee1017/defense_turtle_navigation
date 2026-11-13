import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from turtlesim_msgs.msg import Pose
from std_msgs.msg import Bool


class GoalChecker(Node):

    def __init__(self):
        super().__init__('goal_checker')

        # 목표 좌표 구독
        self.goal_subscriber = self.create_subscription(
            Point,
            '/goal_position',
            self.goal_callback,
            10
        )

        # 현재 위치 구독
        self.pose_subscriber = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # 도착 여부 발행
        self.goal_publisher = self.create_publisher(
            Bool,
            '/goal_reached',
            10
        )

        self.goal_x = 8.0
        self.goal_y = 8.0

        self.current_pose = None
        self.reached = False

        self.timer = self.create_timer(
            0.1,
            self.check_goal
        )

        self.get_logger().info('Goal Checker Started')

    def goal_callback(self, msg):
        self.goal_x = msg.x
        self.goal_y = msg.y

        self.reached = False

    def pose_callback(self, msg):
        self.current_pose = msg

    def check_goal(self):

        if self.current_pose is None:
            return

        dx = self.goal_x - self.current_pose.x
        dy = self.goal_y - self.current_pose.y

        distance = math.sqrt(dx**2 + dy**2)

        msg = Bool()

        if distance < 0.1:
            msg.data = True

            if not self.reached:
                self.get_logger().info('Goal Reached!')

            self.reached = True

        else:
            msg.data = False

        self.goal_publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = GoalChecker()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()