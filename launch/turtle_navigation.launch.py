from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        # Turtlesim 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        # 목표 좌표 발행 노드
        Node(
            package='turtle_navigation',
            executable='goal_publisher',
            name='goal_publisher'
        ),

        # 거북이 제어 노드
        Node(
            package='turtle_navigation',
            executable='turtle_controller',
            name='turtle_controller'
        ),

        # 목표 도착 확인 노드
        Node(
            package='turtle_navigation',
            executable='goal_checker',
            name='goal_checker'
        ),

    ])
