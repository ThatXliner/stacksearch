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
import subprocess
import sys
from typing import List

from stacksearch import errors


def _get_random_sites() -> List[str]:
    SITES = [
        "stackoverflow",
        "serverfault",
        "superuser",
        "meta.stackexchange",
        "webapps.stackexchange",
        "webapps.meta.stackexchange",
        "gaming.stackexchange",
        "gaming.meta.stackexchange",
        "webmasters.stackexchange",
        "webmasters.meta.stackexchange",
        "cooking.stackexchange",
        "cooking.meta.stackexchange",
        "gamedev.stackexchange",
        "gamedev.meta.stackexchange",
        "photo.stackexchange",
        "photo.meta.stackexchange",
        "stats.stackexchange",
        "stats.meta.stackexchange",
        "math.stackexchange",
        "math.meta.stackexchange",
        "diy.stackexchange",
        "diy.meta.stackexchange",
        "meta.superuser",
        "meta.serverfault",
        "gis.stackexchange",
        "gis.meta.stackexchange",
        "tex.stackexchange",
        "tex.meta.stackexchange",
        "askubuntu",
        "meta.askubuntu",
    ]
    return {random.choice(SITES) for x in range(random.randint(1, 3))}


class TestClass:
    """For testing."""

    def main(self, args: str = "") -> None:
        """You should not use this. IT'S A TEST. This is the main function."""
        run_args = [sys.executable, "-m", "stacksearch"]
        run_args.extend(args.split(" "))
        subprocess.run(run_args, check=True)

    def test_stable(self):
        """A test with Search."""
        try:
            self.main('"list"')
        except subprocess.CalledProcessError as error:
            assert error.returncode == 1

    def test_stable_lots_of_sites(self):
        """A test with Search. For lots of sites."""
        try:
            self.main(f'"list" --sites {" ".join(_get_random_sites())}')
        except subprocess.CalledProcessError as error:
            assert error.returncode == 1

    def test_version(self):
        """To test the version."""
        self.main("--version")

    def test_noobs(self):
        """To test the no argument functionality."""
        self.main()
