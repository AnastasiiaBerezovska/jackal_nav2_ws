from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            output='screen',

            remappings=[
                ('cloud_in', '/points_raw'),        # replayed GlobalMap.pcd
                ('scan', '/lonebot/p2s/scan')       # Nav2 + AMCL scan
            ],

            parameters=[{
                'target_frame': 'lonebot/base_link',
                'output_frame': 'lonebot/base_link',
                'transform_tolerance': 0.2,

                # height slicing of the 3D map
                'min_height': 0.1,
                'max_height': 1.5,

                # laser properties
                'angle_min': -3.14159,
                'angle_max':  3.14159,
                'angle_increment': 0.0087,

                'range_min': 0.3,
                'range_max': 30.0,
                'use_inf': True
            }]
        )

    ])
