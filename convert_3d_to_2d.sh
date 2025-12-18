#!/bin/bash
set -e

echo "Starting octomap server..."

ros2 run octomap_server octomap_server_node --ros-args \
  -p resolution:=0.05 \
  -p frame_id:=map \
  -p base_frame_id:=lonebot/base_link \
  -p publish_2d_map:=true \
  -p min_z:=0.0 \
  -p max_z:=1.5 \
  -r cloud_in:=/cloud_pcd &

OCTOMAP_PID=$!
sleep 4

echo "Publishing 3D PCD..."

ros2 run pcl_ros pcd_to_pointcloud --ros-args \
  -p file_name:=/home/robot/jackal_nav2_ws/maps/lio_sam_3d/GlobalMap.pcd \
  -p topic_name:=/cloud_pcd \
  -p tf_frame:=map \
  -p publishing_period_ms:=100 &

PCD_PID=$!
sleep 10

echo "Saving 2D map from /projected_map..."

ros2 run nav2_map_server map_saver_cli \
  -t /projected_map \
  -f /home/robot/jackal_nav2_ws/maps/saved_2d_map

echo "Cleaning up..."
kill $OCTOMAP_PID $PCD_PID
