#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = (
    [
        "typer[all]",
        "rich",
        "boto3",
        "pyyaml",
        "requests",
        "pandas",
        "jinja2",
        "spacy",
        "aiosmtpd",
    ],
)
setup(
    author="Will Thompson",
    author_email="wkt@northwestern.edu",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="MTurk helper code.",
    entry_points={
        "console_scripts": [
            "blab=mturkhelper.cli:app",
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords="mturkhelper",
    name="mturkhelper",
    packages=find_packages(include=["mturkhelper", "mturkhelper.*"]),
    package_data={"mturkhelper": ["data/*"]},
    url="https://github.com/schorndorfer/mturkhelper",
    version="0.1.0",
)
