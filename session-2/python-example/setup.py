#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    author="Will Thompson",
    author_email="wkt@northwestern.edu",
    python_requires=">=3.8",
    description="OpenAI helper code.",
    entry_points={
        "console_scripts": [
            "openaihelper=openaihelper.cli:app",
        ],
    },
    include_package_data=True,
    keywords="OpenAI",
    name="openaihelper",
    packages=find_packages(include=["openaihelper", "openaihelper.*"]),
    package_data={"openaihelper": ["data/*"]},
    version="0.1.0",
)
