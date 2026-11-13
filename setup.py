from setuptools import find_packages, setup

package_name = 'turtle_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            ['launch/turtle_navigation.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lemon',
    maintainer_email='lemon@example.com',
    description='Turtle navigation package',
    license='MIT-0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'goal_publisher = turtle_navigation.goal_publisher:main',
            'turtle_controller = turtle_navigation.turtle_controller:main',
            'goal_checker = turtle_navigation.goal_checker:main',
        ],
    },
)
