#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = (
    [
        "typer[all]",
    ],
)
setup(
    author="Will Thompson",
    author_email="wkt@northwestern.edu",
    python_requires=">=3.8",
    description="OpenAI helper code.",
    entry_points={
        "console_scripts": [
            "openai=openai.cli:app",
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords="OpenAI",
    name="openai_helper",
    packages=find_packages(include=["openai", "openai.*"]),
    package_data={"openai": ["data/*"]},
    version="0.1.0",
)
