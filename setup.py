#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""To setup."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stacksearch-ThatXliner",  # Replace with your own username
    version="1.0.0",
    author="Bryan Hu",
    author_email="bryan.hu.cn@gmail.com",
    description="StackSearch is a python module that provides a way to search StackOverflow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThatXliner/stacksearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
