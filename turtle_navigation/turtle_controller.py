import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point, Twist
from turtlesim_msgs.msg import Pose


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        # 목표 좌표 구독
        self.goal_subscriber = self.create_subscription(
            Point,
            '/goal_position',
            self.goal_callback,
            10
        )

        # 거북이 현재 위치 구독
        self.pose_subscriber = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # 거북이 속도 명령 발행
        self.cmd_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.goal_x = 8.0
        self.goal_y = 8.0

        self.current_pose = None

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.get_logger().info('Turtle Controller Started')

    def goal_callback(self, msg):
        self.goal_x = msg.x
        self.goal_y = msg.y

    def pose_callback(self, msg):
        self.current_pose = msg

    def control_loop(self):

        if self.current_pose is None:
            return

        # 목표 지점까지의 거리
        dx = self.goal_x - self.current_pose.x
        dy = self.goal_y - self.current_pose.y

        distance = math.sqrt(dx**2 + dy**2)

        # 목표 방향 계산
        target_angle = math.atan2(dy, dx)

        # 현재 방향과 목표 방향의 차이
        angle_error = target_angle - self.current_pose.theta

        # 각도 범위 보정
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        cmd = Twist()

        if distance > 0.1:

            cmd.linear.x = min(2.0, 1.5 * distance)
            cmd.angular.z = 4.0 * angle_error

        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_publisher.publish(cmd)


def main(args=None):

    rclpy.init(args=args)

    node = TurtleController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()