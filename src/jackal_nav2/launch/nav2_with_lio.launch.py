from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Path to Nav2 bringup launch file
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    nav2_launch = os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')

    return LaunchDescription([

        # LIO-SAM Nodes
        Node(package='lio_sam', executable='lio_sam_imuPreintegration', output='screen'),
        Node(package='lio_sam', executable='lio_sam_imageProjection', output='screen'),
        Node(package='lio_sam', executable='lio_sam_featureExtraction', output='screen'),
        Node(package='lio_sam', executable='lio_sam_mapOptimization', output='screen'),

        # Delay Nav2 startup ==> waits  for LIO-SAM to publish map/odom
        TimerAction(
            period=12.0,  # Wait 12 seconds before starting Nav2
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(nav2_launch),
                    launch_arguments={
                        'use_sim_time': 'False',
                        'map': '',  # No static YAML map, using LIO-SAM
                        'nav2_subscribe_transient_local': 'True',
                        'yaml_filename': 'True',
                        'odom_topic': '/lio_sam/mapping/odom',
			'map_topic': '/lio_sam/mapping/cloud_registered',
                        'load_route_server': 'False'
                    }.items()
                )
            ]
        ),

        # TF Publishers => static transforms
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'map'],
            output='screen'
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'odom'],
            output='screen'
        ),

        # PointCloud 2D Scan Converter
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='map_to_scan',
            remappings=[
                ('cloud_in', '/lio_sam/mapping/map'),
                ('scan', '/scan')
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
