## My simple Nav Stack
This is my simple nav stack for an iRobot Create2.

Over time, I plan to re-implement most 3rd party nodes and systems myself as programming exercises

This now works with slam

TODO
- Add self-docking feature
- configure system to run at launch
- figure out why the lidar spits out different numbers of points -- maybe fixed with `angle_compensate` parameter
- power the pi from the roomba battery
- implement rtabmap with a depth cam (budget dependant)

DONE
- Add Udev rules to roomba pi

On PC
`ros2 launch slam_toolbox online_sync_launch.py`
`rviz2`

On Robot
`ros2 launch create_bringup create_2.launch`
`ros2 run system_controller system_controller_node`
`ros2 launch rplidar_ros2 view_rplidar_launch.py serial_port:=/dev/ttyUSB1`
