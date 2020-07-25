#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: TEST

Desc: YOU SHOULD NOT USE THIS FILE. IT IS A TEST.

"""
from sys import path
from pathlib import Path

# import httpx

path.insert(0, Path(Path(Path(__file__).parent).parent / "stacksearch"))
from stacksearch.__main__ import custom_main as MAIN


class TestClass:
    """For testing."""

    def main(self, args):
        """You should not use this. IT'S A TEST. This is the main function."""
        MAIN(args)

    def test_one(self):
        """A test with Search."""
        self.main("python list")

    def test_one_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.main("python list --sites superuser.com stackoverflow")

    def test_version(self):
        """To test the version."""
        self.main("-v")
