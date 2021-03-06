"""
VSA package
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name = "ros_holographic",
    version = "0.0.1",
    description = ("HRR ROS package"),
    keywords = "ROS HRR",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Choose your license
    license='FZI',
    install_requires=['numpy']
)
