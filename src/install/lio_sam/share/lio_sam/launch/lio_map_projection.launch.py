from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='map_to_scan',
            remappings=[
                ('cloud_in', '/lio_sam/mapping/map'),  # Input: 3D map from LIO-SAM
                ('scan', '/scan')                      # Output: 2D scan for Nav2
            ],
            parameters=[{
                'min_height': -0.3,
                'max_height': 1.0,
                'angle_increment': 0.0087,
                'range_min': 0.3,
                'range_max': 50.0,
                'use_inf': True
            }]
        )
    ])
