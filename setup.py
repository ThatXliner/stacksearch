#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""To setup."""
from pathlib import Path

from setuptools import find_packages, setup
from stacksearch import __version__

# The directory containing this file
HERE = Path(Path(__file__).parent)

# The text of the README file
README = Path(HERE / "README.md").read_text()
REQUIREMENTS = Path(HERE / "requirements.txt").read_text().split("\n")

setup(
    name="stacksearch",  # Replace with your own username
    version=__version__,
    author="Bryan Hu",
    author_email="bryan.hu.cn@gmail.com",
    description="StackSearch is a python module that "
    "provides a way to search StackOverflow.",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/ThatXliner/stacksearch",
    project_urls={
        "Source Code": "https://github.com/ThatXliner/stacksearch",
        "Documentation": "https://stacksearch.readthedocs.io/en/latest/index.html",
        "Tracker": "https://github.com/ThatXliner/stacksearch/issues",
    },
    packages=find_packages(exclude=["tests"], include=["stacksearch"]),
    # scripts=["scripts/stacksearch"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[line for line in REQUIREMENTS if not line.startswith("#")],
    keywords="api stackexchange stackoverflow python webscrape webscrap",
    entry_points={"console_scripts": ["stacksearch=stacksearch.__main__:cli_main"]},
)
