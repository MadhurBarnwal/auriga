import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # Include the robot state publisher launch file, provided by our own package. Force sim_time to be enabled
    package_name = 'auriga'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
            )]), launch_arguments={'use_sim_time': 'true'}.items()
        )
    
    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        )
    
    # Run the spawner node from the ros_gz_sim package. The entity name doesn't really matter if you only have one robot
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description', 
                                   '-name', 'my_bot',
                                   '-z', '0.1', '-R', '-1.57' ],
                        output='screen')
    

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])