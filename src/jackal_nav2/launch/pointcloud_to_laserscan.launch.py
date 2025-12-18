from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[
                ('cloud_in', '/lio_sam/mapping/cloud_registered'),
                ('scan', '/lonebot/p2s/scan')
            ],
            parameters=[{
                'target_frame': 'lonebot/base_link',
                'output_frame': 'lonebot/base_link',
                'transform_tolerance': 0.2,

                'min_height': -0.3,
                'max_height': 2.0,

                'angle_increment': 0.0087,
                'range_min': 0.3,
                'range_max': 50.0,
                'use_inf': True
            }]
        )
    ])
