#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""To setup."""
from pathlib import Path
from setuptools import setup, find_packages

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="stacksearch-ThatXliner",  # Replace with your own username
    version="1.1.0",
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
)
