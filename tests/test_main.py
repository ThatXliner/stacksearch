#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=R0201
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: TEST

Desc: YOU SHOULD NOT USE THIS FILE. IT IS A TEST.

"""
import random
from typing import List

from stacksearch.__main__ import custom_main as main


def _get_random_sites() -> List[str]:
    SITES = [
        "stackoverflow.com",
        "serverfault.com",
        "superuser.com",
        "meta.stackexchange.com",
        "webapps.stackexchange.com",
        "webapps.meta.stackexchange.com",
        "gaming.stackexchange.com",
        "gaming.meta.stackexchange.com",
        "webmasters.stackexchange.com",
        "webmasters.meta.stackexchange.com",
        "cooking.stackexchange.com",
        "cooking.meta.stackexchange.com",
        "gamedev.stackexchange.com",
        "gamedev.meta.stackexchange.com",
        "photo.stackexchange.com",
        "photo.meta.stackexchange.com",
        "stats.stackexchange.com",
        "stats.meta.stackexchange.com",
        "math.stackexchange.com",
        "math.meta.stackexchange.com",
        "diy.stackexchange.com",
        "diy.meta.stackexchange.com",
        "meta.superuser.com",
        "meta.serverfault.com",
        "gis.stackexchange.com",
        "gis.meta.stackexchange.com",
        "tex.stackexchange.com",
        "tex.meta.stackexchange.com",
        "askubuntu.com",
        "meta.askubuntu.com",
    ]
    return {random.choice(SITES) for x in range(random.randint(1, 3))}


class TestClass:
    """For testing."""

    def main(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main function."""
        main([arg for arg in args.split() if arg])

    def test_stable(self):
        """A test with Search."""
        self.main("python list")

    def test_stable_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        self.main(f"python list --sites {' '.join(_get_random_sites())}")

    def test_version(self):
        """To test the version."""
        self.main("-v")

    def test_noobs(self):
        """To test the no argument functionality."""
        self.main()
