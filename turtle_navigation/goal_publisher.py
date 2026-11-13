import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from std_msgs.msg import Bool


class GoalPublisher(Node):

    def __init__(self):
        super().__init__('goal_publisher')

        self.publisher = self.create_publisher(
            Point,
            '/goal_position',
            10
        )

        self.goal_subscriber = self.create_subscription(
            Bool,
            '/goal_reached',
            self.goal_callback,
            10
        )

        # 순서대로 방문할 목표 좌표
        self.waypoints = [
            (8.0, 8.0),
            (2.0, 8.0),
            (2.0, 2.0),
            (8.0, 2.0)
        ]

        self.current_index = 0
        self.waiting_for_reached = False

        # 첫 번째 목표 발행
        self.timer = self.create_timer(
            1.0,
            self.publish_first_goal
        )

        self.get_logger().info('Goal Publisher Started')

    def publish_first_goal(self):
        self.timer.cancel()
        self.publish_goal()

    def publish_goal(self):

        if self.current_index >= len(self.waypoints):
            return

        x, y = self.waypoints[self.current_index]

        msg = Point()
        msg.x = x
        msg.y = y
        msg.z = 0.0

        self.publisher.publish(msg)

        self.waiting_for_reached = True

        self.get_logger().info(
            f'Goal {self.current_index + 1}: ({x}, {y})'
        )

    def goal_callback(self, msg):

        if not msg.data or not self.waiting_for_reached:
            return

        self.waiting_for_reached = False
        self.current_index += 1

        if self.current_index >= len(self.waypoints):
            self.get_logger().info('All Waypoints Completed!')
            return

        self.get_logger().info('Moving to Next Waypoint')

        self.next_timer = self.create_timer(
            0.5,
            self.publish_next_goal
        )

    def publish_next_goal(self):
        self.next_timer.cancel()
        self.publish_goal()


def main(args=None):

    rclpy.init(args=args)

    node = GoalPublisher()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
