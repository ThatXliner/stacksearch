#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: see __init__.py

Desc: The errors stacksearch may raise.

"""


class UnsupportedPythonVersion(Exception):
    """
    This error is raised when your python version is not supported.
    This may be thrown if your python version is below verison 3.8.
    """
