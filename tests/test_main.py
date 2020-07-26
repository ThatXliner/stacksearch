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
from asyncio import run

# import httpx

path.insert(0, Path(Path(Path(__file__).parent).parent / "stacksearch"))
from stacksearch.__main__ import custom_main as MAIN
from stacksearch.__main__ import fcustom_main as FMAIN


class TestClass:
    """For testing."""

    def main(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main function."""
        MAIN([arg for arg in args.split() if arg])

    def amain(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main async function."""
        run(FMAIN([arg for arg in args.split() if arg]))

    def test_stable(self):
        """A test with Search."""
        self.main("python list")

    def test_async(self):
        """To test the async search."""
        self.amain("python list")

    def test_stable_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.main("python list --sites superuser.com stackoverflow")

    def test_async_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.amain("python list --sites superuser.com stackoverflow")

    def test_version(self):
        """To test the version."""
        self.main("-v")

    def test_async_version(self):
        """To test the version."""
        self.amain("-v")

    def test_noobs(self):
        """To test the no argument functionality."""
        self.main()

    def test_async_noobs(self):
        """To test the no argument functionality."""
        self.amain()
