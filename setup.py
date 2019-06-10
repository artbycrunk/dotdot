#!/usr/bin/env python3

from setuptools import setup

setup(
    name="dotdot",
    version="0.1.0",
    description="A cross platform dotfiles manager",
    author="Savio Fernandes",
    author_email="savio@saviof.com",
    license="MIT",
    url="https://github.com/artbycrunk/dotdot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    packages=[
        "dotdot"
    ],
    install_requires=[
        "argparse",
    ],
    entry_points="""
    [console_scripts]
    dotdot=dotdot.cli:main
    """,
)
