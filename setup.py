from setuptools import setup

package_name = 'team99_chase_object'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tony',
    maintainer_email='jarobledo98@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'detect_object = team99_chase_object.detect_object:main',
            'get_object_range = team99_chase_object.get_object_range:main',
        ],
    },
)
