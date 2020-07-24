#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""To setup."""
from pathlib import Path
from setuptools import setup, find_packages
from stacksearch.__init__ import __version__

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
REQUIREMENTS = (HERE / "requirements.txt").read_text().split("\n")

setup(
    name="stacksearch",  # Replace with your own username
    version=__version__,
    author="Bryan Hu",
    author_email="bryan.hu.cn@gmail.com",
    description="StackSearch is a python module that provides a way to search StackOverflow.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ThatXliner/stacksearch",
    packages=find_packages(exclude="tests", include="stacksearch"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[line for line in REQUIREMENTS if not line.startswith("#")],
)
